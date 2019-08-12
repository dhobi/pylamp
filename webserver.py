import sys
import json
import lamphw
import remote
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.resource import Resource

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
	WebSocketClientProtocol, \
	WebSocketClientFactory, \
	connectWS

from autobahn.twisted.resource import WebSocketResource


class ApplicationConstants:
    myLamp = lamphw.LampHw(16, 20, 21, True, 255)
    colormessage = "color"
    powermessage = "power"
    typemessage = "type"
    periodmessage = "period"
    rgbmessage = "rgb"

    @staticmethod
    def broadcastLamp(factory):
        factory.broadcast(
            '{"timerPeriod": ' + str(ApplicationConstants.myLamp.timerPeriod) + ',"timerName": "' + str(
                ApplicationConstants.myLamp.timerName) + '","isOn":' + str(
                ApplicationConstants.myLamp.ISRUNNING).lower() + ', "red":' + str(
                ApplicationConstants.myLamp.webRed) + ', "green":' + str(
                ApplicationConstants.myLamp.webGreen) + ', "blue":' + str(ApplicationConstants.myLamp.webBlue) + ' }')

    @staticmethod
    def setFromJson(data):
        value = data['value']
        if data['message'] == ApplicationConstants.colormessage:
            ApplicationConstants.myLamp.color(value['r'], value['g'], value['b'])
        elif data['message'] == ApplicationConstants.powermessage:
            ApplicationConstants.myLamp.toggle()
        elif data['message'] == ApplicationConstants.typemessage:
            ApplicationConstants.myLamp.type(value['name'])
        elif data['message'] == ApplicationConstants.periodmessage:
            ApplicationConstants.myLamp.period(value['period'])

class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        data = json.loads(payload)
        print("New message:" + payload)
        ApplicationConstants.setFromJson(data)
        ApplicationConstants.broadcastLamp(self.factory)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))
            print("message sent to {}".format(c.peer))


class ColorPage(Resource):
    def __init__(self, factory):
        Resource.__init__(self)
        self.factory = factory

    def render_GET(self):
        return ''

    def render_POST(self, request):
        try:
            data = json.loads(request.content.getvalue())
            ApplicationConstants.myLamp.color(data['r'], data['g'], data['b'])
            ApplicationConstants.broadcastLamp(self.factory)
            return ''
        except:
            return sys.exc_info()[0]


class PowerPage(Resource):
    def __init__(self, factory):
        Resource.__init__(self)
        self.factory = factory

    def render_GET(self):
        return ''

    def render_POST(self, request):
        ApplicationConstants.myLamp.toggle()
        ApplicationConstants.broadcastLamp(self.factory)
        return ''


class PeriodPage(Resource):
    def __init__(self, factory):
        Resource.__init__(self)
        self.factory = factory

    def render_GET(self):
        return ''

    def render_POST(self, request):
        data = json.loads(request.content.getvalue())
        ApplicationConstants.myLamp.type(data['name'])
        ApplicationConstants.myLamp.period(data['period'])
        ApplicationConstants.broadcastLamp(self.factory)
        return ''


class RgbPage(Resource):
    def __init__(self, factory):
        Resource.__init__(self)
        self.factory = factory

    def render_GET(self, request):
        if 'format' in request.args:
            hexRed = "%0.2X" % ApplicationConstants.myLamp.webRed
            hexGreen = "%0.2X" % ApplicationConstants.myLamp.webGreen
            hexBlue = "%0.2X" % ApplicationConstants.myLamp.webBlue
            print("hexRed:"+hexRed)
            print("hexGreen:"+hexGreen)
            print("hexblue:"+hexBlue)
            return hexRed+hexGreen+hexBlue
        if 'color' in request.args:
            hexColor = request.args['color'][0]
            rgb = tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))
            ApplicationConstants.myLamp.color(rgb[0], rgb[1], rgb[2])
            ApplicationConstants.broadcastLamp(self.factory)
            return ''
        return 'unknown request'

    def render_POST(self, request):
        return ''

class RemoteControl:
    currentIndex = 0
    animationList = ["off", "blinking", "pulsating", "rainbow"]

    def __init__(self, factory):
        self.factory = factory

    def onRemote(self, key):
        if key == "KEY_POWER":
            ApplicationConstants.myLamp.toggle()
        elif key == "KEY_A":
            ApplicationConstants.myLamp.color(255, 0, 0)
        elif key == "KEY_B":
            ApplicationConstants.myLamp.color(0, 255, 0)
        elif key == "KEY_C":
            ApplicationConstants.myLamp.color(0, 0, 255)
        elif key == "KEY_RIGHT":
            self.currentIndex = self.currentIndex + 1
            if self.currentIndex == len(self.animationList):
                self.currentIndex = 0
            ApplicationConstants.myLamp.type(self.animationList[self.currentIndex])
        elif key == "KEY_LEFT":
            self.currentIndex = self.currentIndex - 1
            if self.currentIndex < 0:
                self.currentIndex = len(self.animationList) - 1
            ApplicationConstants.myLamp.type(self.animationList[self.currentIndex])
        elif key == "KEY_UP":
            currentPeriod = ApplicationConstants.myLamp.timerPeriod
            if currentPeriod < 5.0:
                currentPeriod = currentPeriod + 0.1
            ApplicationConstants.myLamp.period(currentPeriod)
        elif key == "KEY_DOWN":
            currentPeriod = ApplicationConstants.myLamp.timerPeriod
            if currentPeriod > 0.15:
                currentPeriod = currentPeriod - 0.1
            ApplicationConstants.myLamp.period(currentPeriod)

        ApplicationConstants.broadcastLamp(self.factory)

class MyClientProtocol(WebSocketClientProtocol):
    def __init__(self, factory):
        WebSocketClientProtocol.__init__(self)
        self.serverFactory = factory
    def onMessage(self, payload, isBinary):
        print("New message from websocket.in:" + payload)
        try:
            data = json.loads(payload)

            if 'message' in data:
                ApplicationConstants.setFromJson(data)
                ApplicationConstants.broadcastLamp(self.serverFactory)
            else:
                ApplicationConstants.myLamp.period(0.5)
                if data['build']['status'] == 'SUCCESS':
                    ApplicationConstants.myLamp.color(0, 255, 0)
                elif data['build']['status'] == 'UNSTABLE':
                    ApplicationConstants.myLamp.color(255, 255, 0)
                elif data['build']['status'] == 'ABORTED':
                    ApplicationConstants.myLamp.color(0, 0, 255)
                else:
                    ApplicationConstants.myLamp.color(255, 0, 0)
                if data['build']['phase'] == 'COMPLETED':
                    ApplicationConstants.myLamp.type('off')
                else:
                    ApplicationConstants.myLamp.type('pulsating')
                ApplicationConstants.broadcastLamp(self.serverFactory)
        except BaseException as e:
            print("Failed to parse:" + payload + " because " + str(e))

def destroy():
    ApplicationConstants.myLamp.destroy()
    remoteDaemon.destroy()

if __name__ == "__main__":
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File("/home/pi/pylamp/web")

    factory = BroadcastServerFactory(u"ws://127.0.0.1:80")
    factory.protocol = BroadcastServerProtocol
    resource = WebSocketResource(factory)
    root.putChild(u"ws", resource)

    remoteControl = RemoteControl(factory)
    remoteDaemon = remote.Remote(remoteControl.onRemote)

    root.putChild(ApplicationConstants.colormessage, ColorPage(factory))
    root.putChild(ApplicationConstants.powermessage, PowerPage(factory))
    root.putChild(ApplicationConstants.periodmessage, PeriodPage(factory))
    root.putChild(ApplicationConstants.rgbmessage, RgbPage(factory))

    site = Site(root)
    
    factoryClient = WebSocketClientFactory(u"wss://connect.websocket.in/pylamp?room_id=1")
    factoryClient.protocol = lambda: MyClientProtocol(factory)
    connectWS(factoryClient)
    
    reactor.addSystemEventTrigger('during', 'shutdown', destroy)
    reactor.listenTCP(80, site)
    reactor.run()

import sys
import json
import lamp
import setinterval
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.resource import Resource

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


class ApplicationConstants:
    myLamp = lamp.Lamp()
    colormessage = "color"
    powermessage = "power"
    typemessage = "type"
    periodmessage = "period"

    @staticmethod
    def broadcastLamp(factory):
        factory.broadcast(
            '{"timerPeriod": ' + str(ApplicationConstants.myLamp.timerPeriod) + ',"timerName": "' + str(
                ApplicationConstants.myLamp.timerName) + '","isOn":' + str(
                ApplicationConstants.myLamp.ISRUNNING).lower() + ', "red":' + str(
                ApplicationConstants.myLamp.webRed) + ', "green":' + str(
                ApplicationConstants.myLamp.webGreen) + ', "blue":' + str(ApplicationConstants.myLamp.webBlue) + ' }')


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        data = json.loads(payload)
        value = data['value']
        print("New message:"+payload)
        if data['message'] == ApplicationConstants.colormessage:
            ApplicationConstants.myLamp.color(value['r'], value['g'], value['b'])
        elif data['message'] == ApplicationConstants.powermessage:
            ApplicationConstants.myLamp.toggle()
        elif data['message'] == ApplicationConstants.typemessage:
            ApplicationConstants.myLamp.type(value['name'])
        elif data['message'] == ApplicationConstants.periodmessage:
            ApplicationConstants.myLamp.period(value['period'])
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


if __name__ == "__main__":
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File("./web")

    factory = BroadcastServerFactory(u"ws://127.0.0.1:80")
    factory.protocol = BroadcastServerProtocol
    resource = WebSocketResource(factory)
    root.putChild(u"ws", resource)

    root.putChild(ApplicationConstants.colormessage, ColorPage(factory))
    root.putChild(ApplicationConstants.powermessage, PowerPage(factory))

    site = Site(root)
    reactor.addSystemEventTrigger('during', 'shutdown', ApplicationConstants.myLamp.destroy)
    reactor.listenTCP(80, site)
    reactor.run()

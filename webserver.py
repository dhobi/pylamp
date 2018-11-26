import sys
import json
import lamp
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

from autobahn.twisted.resource import WebSocketResource


class LampHolder:
    myLamp = lamp.Lamp()


def clean():
    LampHolder.myLamp.destroy()


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.factory.register(self)

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onMessage(self, payload, isBinary):
        data = json.loads(payload)
        value = data['value']
        if data['message'] == 'color':
            LampHolder.myLamp.color(value['r'], value['g'], value['b'])
        elif data['message'] == 'power':
            LampHolder.myLamp.toggle()

        self.factory.broadcast('{"isOn":' + str(LampHolder.myLamp.ISRUNNING).lower() + ', "red":' + str(
                LampHolder.myLamp.currentred * 2.55) + ', "green":' + str(
                LampHolder.myLamp.currentgreen * 2.55) + ', "blue":' + str(LampHolder.myLamp.currentblue * 2.55) + ' }')

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


if __name__ == "__main__":
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File("./web")

    factory = BroadcastServerFactory(u"ws://127.0.0.1:80")
    factory.protocol = BroadcastServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.addSystemEventTrigger('during', 'shutdown', clean)
    reactor.listenTCP(80, site)
    reactor.run()

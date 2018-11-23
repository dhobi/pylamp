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


class SomeServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("some request connected {}".format(request))

    def onMessage(self, payload, isBinary):
        colors = json.loads(payload)
        LampHolder.myLamp.color(colors['r'], colors['g'], colors['b'])


def clean():
    LampHolder.myLamp.destroy()


if __name__ == "__main__":
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File("./web")

    factory = WebSocketServerFactory(u"ws://127.0.0.1:80")
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(u"ws", resource)

    site = Site(root)
    reactor.addSystemEventTrigger('during', 'shutdown', clean)
    reactor.listenTCP(80, site)
    reactor.run()

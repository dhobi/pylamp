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


class SomeServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        self.lamp = lamp.Lamp()
    def onConnect(self, request):
        print("some request connected {}".format(request))

    def onMessage(self, payload, isBinary):
        colors = json.loads(payload)
        self.lamp.color(colors.r, colors.g, colors.b)
        self.sendMessage("message received")


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
    reactor.listenTCP(80, site)
    reactor.run()
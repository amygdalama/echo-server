from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint


class Echo(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols += 1
        self.transport.write(
            "Welcome! There are currently %d open connections." %
            self.factory.numProtocols)

    def connectionLost(self, reason):
        self.factory.numProtocols -= 1

    def dataReceived(self, data):
        self.transport.write(data)


class EchoFactory(Factory):

    def __init__(self):
        self.numProtocols = 0

    def buildProtocol(self, addr):
        return Echo(self)


if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 8007)
    endpoint.listen(EchoFactory())
    reactor.run()

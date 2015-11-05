#!/usr/bin/env python
import zmq
import time
import socket
from Showtime.zst_node import ZstNode
from zeroconf import ServiceInfo, Zeroconf


class ZstStage(ZstNode):

    def __init__(self, stageName="stage", port=6000):
        ZstNode.__init__(self, stageName)
        self.zeroconf = Zeroconf()

        address = "tcp://*:" + str(port)
        self.reply.socket.bind(address)

        desc = {'name': self.name}
        addr = socket.gethostbyname(socket.gethostname())
        servicename = "ShowtimeStage"
        self.stageServiceInfo = ServiceInfo("_zeromq._tcp.local.",
           servicename + "._zeromq._tcp.local.",
           socket.inet_aton(addr), port, 0, 0,
           desc)
        self.zeroconf.register_service(self.stageServiceInfo)
        print("Stage active on address " + str(self.reply.socket.getsockopt(zmq.LAST_ENDPOINT)))
        
    def close(self):
        self.zeroconf.unregister_service(self.stageServiceInfo)
        self.zeroconf.close()
        ZstNode.close(self)


if __name__ == '__main__':
    stage = ZstStage()
    stage.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stage.close()

    print("Finished")

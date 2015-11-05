import threading
import zmq
import json
try:
    import queue
except ImportError:
    import Queue as queue
from Showtime.zst_base import ZstBase
from Showtime.zst_method import ZstMethod


class ZstSocket(threading.Thread):

    def __init__(self, ctx, sockettype, sharedqueue, name=None):
        threading.Thread.__init__(self, name=name)
        self.ctx = ctx
        self.exitFlag = 0
        self.poller = None
        self.name = name if name else "socket"
        self.setDaemon(True)

        self.socket = self.ctx.socket(sockettype)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.inMailbox = sharedqueue
        self.outMailbox = queue.Queue()

        if sockettype == zmq.REP or sockettype == zmq.SUB:
            self.poller = zmq.Poller()
            self.poller.register(self.socket, zmq.POLLIN)

        self.start()

    def stop(self):
        self.exitFlag = 1
        self.join(ZstBase.TIMEOUT)

    def run(self):
        while not self.exitFlag:
            if self.poller:
                self.handle_requests()
            else:
                self.handle_outgoing()
        print(self.name + " received kill signal")
        self.socket.close()

    def handle_outgoing(self):
        try:
            message = self.outMailbox.get(True, ZstBase.TIMEOUT)
        except queue.Empty:
            return
        self.send_immediate(message.method, message.data)

    def handle_requests(self):
        if self.poller:
            socklist = dict(self.poller.poll(ZstBase.TIMEOUT))
            for socket in socklist:
                message = self.recv_immediate(zmq.DONTWAIT)
                if message:
                    self.inMailbox.put(message)

    def send(self, method, methodData=None):
        self.outMailbox.put(MethodMessage(method, methodData))

    def send_immediate(self, method, methodData=None):
        try:
            outData = {}
            if methodData:
                outData = methodData.as_dict()
            self.socket.send_multipart(
                [method.encode("utf-8"), json.dumps(outData).encode("utf-8")])
        except Exception as e:
            print(e)

    def recv(self):
        try:
            return self.inMailbox.get(True, ZstBase.TIMEOUT)
        except Queue.Empty:
            return None

    def recv_immediate(self, noblock=None):
        try:
            msg = self.socket.recv_multipart(
                zmq.NOBLOCK) if noblock else self.socket.recv_multipart()
            method = msg[0].decode('utf-8')
            method = method if method else None
            methodBytes = msg[1]
            methodStr = methodBytes.decode('utf-8') if methodBytes else None
            data = json.loads(methodStr) if methodStr else None
            if data:
                methodData = ZstMethod(
                    name=data[ZstMethod.METHOD_NAME],
                    node=data[ZstMethod.METHOD_ORIGIN_NODE],
                    accessMode=data[ZstMethod.METHOD_ACCESSMODE],
                    args=data[
                        ZstMethod.METHOD_ARGS] if ZstMethod.METHOD_ARGS in data else None,
                    output=data[ZstMethod.METHOD_OUTPUT] if ZstMethod.METHOD_OUTPUT in data and data[ZstMethod.METHOD_OUTPUT] else None)
                return MethodMessage(method=method, data=methodData)
            else:
                return MethodMessage(method=method, data=data)
        except zmq.ZMQError as e:
            print(e)
        return None


class MethodMessage():

    def __init__(self, method, data):
        self.method = method
        self.data = data

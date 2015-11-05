import zmq
import threading
try:
    import queue
except ImportError:
    import Queue as queue

class ZstBase(threading.Thread):

    TIMEOUT = 1.0

    def __init__(self, name=None):
        threading.Thread.__init__(self, name=name)

        self.id = name
        self.exitFlag = 0
        self.setDaemon(True)

        # Create queue
        self.incomingQueue = queue.Queue()
        self.ctx = zmq.Context()

    def run(self):
        self.listen()

    def close(self):
        self.exitFlag = 1
        self.ctx.destroy()
        print("\nCleanup complete")

    def listen(self):
        print("Node listening for requests...")
        while not self.exitFlag:
            try:
                message = self.incomingQueue.get(True, ZstBase.TIMEOUT)
                if message:
                    self.receive_message(message)
            except queue.Empty:
                pass
        self.join()

    def receive_message(self, message):
        raise NotImplementedError

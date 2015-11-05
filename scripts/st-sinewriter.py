#!/usr/bin/env python
import sys
import math
import time
import threading
from Showtime.zst_node import *

# Convert Python inputs
if sys.version[0] == "3":
    raw_input = input

def listStageNodes(nodelist): 
    print("Nodes on stage:")
    print("---------------")
    for name, peer in list(nodelist.items()):
        print("Node: " + name)
        for methodname, method in list(peer.methods.items()):
            print(methodname + " " + json.dumps(method.as_dict(), indent=1, sort_keys=True))


class Sinewave(threading.Thread):

    def __init__(self, reader, node, method, args, scale):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.reader = reader
        self.args = args
        self.exitFlag = 0
        self.node = node
        self.method = method
        self.scale = scale

    def stop(self):
        self.exitFlag = 1

    def run(self):
        count = 0
        while not self.exitFlag:
            count += 0.01
            count = count % 100
            value = (math.sin(count) + 1) * 0.5 * self.scale
            print value
            self.args["value"] = value
            self.reader.update_remote_method(
                self.node.methods[self.method], self.args)
            time.sleep(0.01)


if __name__ == '__main__':
    reader = ZstNode("SinewaveWriter", sys.argv[1])
    reader.start()

    scale = 1.0
    if len(sys.argv) > 2:
        scale = float(sys.argv[2])

    nodeList = reader.request_node_peerlinks()
    listStageNodes(nodeList);

    nodeName = raw_input("Enter a node to connect to: ")
    methodName = raw_input("Enter a method to control: ")

    if nodeName in nodeList:
        node = nodeList[nodeName]
        reader.subscribe_to(node)
        reader.connect_to_peer(node)

        time.sleep(1)

        args = {}
        for argname, argvalue in list(node.methods[methodName].args.items()):
            args[argname] = raw_input(
                "Enter a value for the argument " + str(argname) + ": ")

        sinewave = Sinewave(reader, node, methodName, args, scale)
        sinewave.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            sinewave.stop()
            reader.close()
            print("\nExiting...")

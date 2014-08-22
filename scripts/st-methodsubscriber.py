#!/usr/bin/env python
import sys
import time
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


if __name__ == '__main__':
    def echo_method(methodData):
        print("Method: " + str(methodData.name) + " Arguments: " +
              str(methodData.args) + " Output: " + str(methodData.output))

    subscriber = ZstNode("MethodSubscriber", sys.argv[1])
    subscriber.start()
    nodeList = subscriber.request_node_peerlinks()
    listStageNodes(nodeList)

    nodeName = raw_input("Enter a node to connect to: ")
    methodName = raw_input("Enter a method to subscribe to: ")

    if nodeName in nodeList:
        node = nodeList[nodeName]
        subscriber.subscribe_to(node)
        subscriber.connect_to_peer(node)
        subscriber.subscribe_to_method(node.methods[methodName], echo_method)
        subscriber.listen()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        subscriber.close()
        print("Finished")

#!/usr/bin/env python
import sys
import time
import json
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


# Test cases
if __name__ == '__main__':
    reader = ZstNode("MethodEditor", sys.argv[1])
    reader.start()
    nodeList = reader.request_node_peerlinks()
    listStageNodes(nodeList)

    nodeName = raw_input("Enter a node to connect to: ")
    methodName = raw_input("Enter a method to control: ")

    if nodeName in nodeList:
        node = nodeList[nodeName]
        reader.subscribe_to(node)
        reader.connect_to_peer(node)

        time.sleep(1)

        count = 0
        try:
            while True:
                args = {}
                if len(node.methods[methodName].args) > 0:
                    for argname, argvalue in list(node.methods[methodName].args.items()):
                        args[argname] = raw_input(
                            "Enter a value for the argument " + str(argname) + ": ")
                result = reader.update_remote_method(
                    node.methods[methodName], args)
                if result:
                    print(json.dumps(result.output, indent=1, sort_keys=True))
                time.sleep(1)
        except KeyboardInterrupt:
            reader.close()
            print("Exiting")

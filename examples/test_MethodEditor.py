import sys
import time
import json
from Showtime.zst_node import *
import test_base

# Convert Python inputs
if sys.version[0] == "3":
    raw_input = input

reader = ZstNode("MethodEditor", sys.argv[1])
reader.start()
nodeList = reader.request_node_peerlinks()
test_base.listStageNodes(nodeList)

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

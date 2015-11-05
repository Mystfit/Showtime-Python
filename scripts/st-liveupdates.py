#!/usr/bin/env python
import sys
import time
import Queue
from Showtime.zst_node import *

if __name__ == '__main__':
    def list_updates(methodData):
        updateQueue.put(methodData.output)

    subscriber = ZstNode("MethodSubscriber", sys.argv[1])
    subscriber.start()
    nodeList = subscriber.request_node_peerlinks()

    updateQueue = Queue.Queue()

    nodeName = "LiveNode"
    methodName = "layout_updated"

    node = nodeList[nodeName]
    subscriber.subscribe_to(node)
    subscriber.connect_to_peer(node)
    subscriber.subscribe_to_method(node.methods[methodName], list_updates)
    # subscriber.start()
        
    try:
        while True:
            update = updateQueue.get(timeout=1000)
            if update:
                print("===== Start Update =====")
                removeCount = 0
                addCount = 0
                for i in update:
                    print ("ID: %s, Status: %s" % (i["id"], i["status"]))
                    if i["status"] == "added":
                        addCount += 1
                    if i["status"] == "removed":
                        removeCount += 1
                print("----- End Update %s added, %s removed -----\n" % (addCount, removeCount))
    except KeyboardInterrupt:
        subscriber.close()
        print("Finished")

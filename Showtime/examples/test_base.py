import json

def listStageNodes(nodelist): 
	print("Nodes on stage:")
	print("---------------")
	for name, peer in list(nodelist.items()):
	    print("Node: " + name)
	    for methodname, method in list(peer.methods.items()):
	        print(methodname + " " + json.dumps(method.as_dict(), indent=1, sort_keys=True))
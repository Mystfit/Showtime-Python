Showtime-Python
===============

What is this?
-------------
Showtime was designed to let multiple programs running in multiple languages talk to each other whilst trying to cut down on the clutter required in setting up connections and discovering each other. 

The project originated from wanting to bypass the hassles I was having when trying to hook the music software Ableton Live up to Unity using OSC. I wrote the first version of this library using Python and C# to let Unity control Ableton Live through its underlying Python API, without needing to use any MIDI or OSC whatsoever, and that eventually evolved into the Java and Processing ports as well.

### Requirements ###
 - Python 2.7

Installation
---------------------
- Using pip:
```
pip install Showtime-Python
```
- From source:
```
python setup.py install
```


### Notable scripts ###
 - Showtime/zst_stage.py - Creates a stage on port 6000.
 - Showtime/tests/test_MethodEditor.py - Commandline prompt that controls remote node methods directly.
 - Showtime/tests/test_MethodSubscriber.py - Commandline prompt that listens to specific messages from a remote node.
 - Showtime/tests/test_SinewaveWriter.py - Writes a constant sinewave to a remote node method.

Usage
-----

### Setup ###
 - Set up the Stage node. This is to provide a fixed point that all nodes need to register their addresses and methods to upon startup, so that they can be discovered by other nodes. A quick way to get a stage running is to run the included `zst_stage.py` script. This will create a stage on port 6000.
 - Import the libraries.
```
from Showtime.zst_node import *
```
 - Create a new node with a unique name and the address/port of the stage.
```
localNode = ZstNode("ExampleNode", "tcp://127.0.0.1:6000")
localNode.start()
```

### Exploring the stage ###
 - Get a lost of all availble nodes and their methods from the stage.
```
peerList = localNode.request_node_peerlinks()
```

### Listening to other nodes ###
 - If we want to listen to messages being sent from another node, subscribe to the node and assign local callback functions that will run when messages of that type arrive.
```
remoteNode = nodeList["remote_node_name"]
localNode.subscribe_to(remoteNode)
localNode.subscribe_to_method(remoteNode.methods["remote_method_name"], callbackMethod)
```
 - The callback function needs to accept a single ZstMethod argument, which is the method object sent by the remote node.
```
def callbackMethod(methodData):
 print(meterData.name)         // Name of method
 print(meterData.node)         // Name of origin node this method belongs to
 print(meterData.accessMode)   // Type of method: read, write or responder
 print(meterData.args)         // Arguments remote method accepts. Dictionary of Strings/Objects.
 print(meterData.output)       // Output of remote method. 
```

### Controlling remote nodes ###
 - If we want to control a remote node, we have to ask it to listen to messages that we send its way.
```
localNode.connect_to_peer(remoteNode)

// Need to wait a few ms for the remote node to connect
// else it loses the first bunch of messages 
time.sleep(0.1)
```
 - When calling a remote method, we need to provide a dictionary of Strings/Objects containing the arguments that we're sending.
```
localNode.update_remote_method(remoteNode.methods["some_remote_method], {"arg1": 0, "arg2": "some_string"})
```
 - When working with methods where the accessmode is a responder, the `update_remote_method()` call will return a ZstMethod containing the output of the method. Something to be aware of is that if the remote node doesn't send back a response, the program may wait indefinitely. This will be fixed in a future release.
```
result = localNode.update_remote_method(remoteNode.methods["some_remote_method], {"arg1": 0, "arg2": "some_string"})
print(result.output)
```

### Registering local methods ###
 - To register a local method for other nodes to control, you need to provide the method name, the accessmode, the arguments required when calling the method, and the name of the callback method to run. The callback needs to accept a ZstMethod object in order to access incoming arguments.
```
//Read only local method
localNode.request_register_method("local_method", ZstMethod.READ)

//Writeable local method, responder is identical but uses ZstMethod.RESPONDER.
localNode.request_register_method("local_method", ZstMethod.WRITE, {"arg1":None, "arg2":None}, localCallback)

def localCallback(methodData):
  print(methodData.args["arg1"])
}
```

### Updating local methods ###
- When we've run a local method, we need to let any listening nodes know that the method was called.
```
localNode.request_register_method("foo", ZstMethod.READ)

void foo(String someMessage){
 localNode.update_local_method(node.methods["foo"], someMessage)
}
```
- We can update local methods by name as well.
```
localNode.update_local_method_by_name("foo", someMessage)
```


### Accessmode types ###
- `ZstMethod.READ`: Can subscribe to messages from this remote method, but cannot call it.
- `ZstMethod.WRITE`: Can call this remote method but cannot listen to messages it sends.
- `ZstMethod.RESPONDER`: Can call this remote method and receive a response. This is the most similar to how you would usually call a local method.


Contributing
------------
If you want to modify/compile the library iteslf then feel free! If you do decide to use this library or Showtime in general then feel free to flick me a message, I'd appreciate any feedback!


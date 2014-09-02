try:
    import rtmidi_python as rtmidi
except ImportError:
    import rtmidi

from Showtime.zst_node import ZstNode
from Showtime.zst_method import ZstMethod

import time, sys, platform
from optparse import OptionParser


class MidiNode(ZstNode):

    NOTE_ON = 0x90
    NOTE_OFF = 0x80

    MIDI_IN = "in"
    MIDI_OUT = "out"

    def __init__(self, nodename, stageAddress, midiPortOut=None, midiPortIn=None):
        ZstNode.__init__(self, nodename, stageAddress)

        # Setup midi port 
        self.midi_out = None
        self.midi_in = None

        self.midi_out = self.createMidi(MidiNode.MIDI_OUT, midiPortOut)
        self.midi_in = self.createMidi(MidiNode.MIDI_IN, midiPortIn)

        if self.midi_in:
            self.midi_in.callback = self.midi_from_device

        # Note tracking
        self.activeNotes = {}
        self.lastNote = None
        self.isMonophonic = True

    def init(self):
        self.start()
        self.request_register_node()
        self.request_register_method("midi_from_device", ZstMethod.READ)
        self.request_register_method("midi_from_network", ZstMethod.WRITE, 
            {"status": 0, "dataA":0, "dataB":0}, 
            self.midi_from_network)

    def midiOutActive(self):
        if self.midi_out:
            return True
        return False

    def midiInActive(self):
        if self.midi_in:
            return True
        return False

    def createMidi(self, porttype, midiportindex=None):
        # Midi startup. Try creating a virtual port. Doesn't work on Windows
        midi = None
        if porttype == MidiNode.MIDI_IN:
            midi = rtmidi.MidiIn()
        elif porttype == MidiNode.MIDI_OUT:
            midi = rtmidi.MidiOut()
        else:
            return None

        if midiportindex < 0:
            if platform.system() == "Windows":
                print "Can't open virtual midi port on windows. Try using loopMidi."
            else:
                midi.open_virtual_port("Showtime-Midi-" + porttype)
        else:
            print "Opening midi " + str(porttype) + " port " + str(midiportindex)
            midi.open_port(midiportindex)

        return midi


    def listMidiOutPorts(self):
        print("Available Midi Out ports:")
        portindex = 0
        if self.midi_out:
            for port in self.midi_out.ports:
                print str(portindex) + ": " + str(port)
                portindex += 1

    def listMidiInPorts(self):
        print("Available Midi In ports:")
        portindex = 0
        if self.midi_in:
            for port in self.midi_in.ports:
                print str(portindex) + ": " + str(port)
                portindex += 1

    # def play_note(self, message):
    #     trigger = MidiNode.NOTE_ON
    #     velocity = int(message.args["velocity"])
    #     note = int(message.args["note"])

    #     if self.midi_out:
    #         self.midi_out.send_message([trigger, int(message.args["note"]), velocity])

    def midi_from_device(self, message, timestamp):
        print message
        self.update_local_method_by_name("midi_from_device", {"status":message[0], "dataA":message[1], })

        # if self.midi_out:
        #     self.midi_out.send_message([message[0], message[1], message[2]])

    def midi_from_network(self, message, timestamp):
        int(message.args["status"])
        int(message.args["dataA"])
        int(message.args["dataB"])
        if self.midi_out:
            self.midi_out.send_message([trigger, int(message.args["note"]), velocity])


if __name__ == '__main__':
    
    # Options parser
    parser = OptionParser()
    parser.add_option("-s", "--stagehost", action="store", dest="stageaddress", type="string", help="IP address of the Showtime stage.", default="localhost")
    parser.add_option("-p", "--stageport", action="store", dest="stageport", type="string", help="Port of the Showtime stage", default="6000")
    parser.add_option("--virtual", action="store_true", dest="virtualports", help="Create virtual midi ports", default=False)
    parser.add_option("--im", "--inmidi", action="store", dest="inmidi", type="int", help="Midi in port", default=0)
    parser.add_option("--om", "--outmidi", action="store", dest="outmidi", type="int", help="Midi out port", default=0)
    parser.add_option("--listmidiports", action="store_true", dest="listmidiports", help="List the available midi ports on the system.", default=False)
    (options, args) = parser.parse_args()

    midiNode = None
    nodename = "KP3"
    stageaddress = options.stageaddress + ":" + str(options.stageport)

    print stageaddress

    if options.listmidiports:
        midiNode = MidiNode(nodename, stageaddress)
        midiNode.listMidiOutPorts()
        midiNode.listMidiInPorts()
        sys.exit(0)

    if options.virtualports:
        midiNode = MidiNode(nodename, stageaddress)
    else:
        midiNode = MidiNode(nodename, stageaddress, options.outmidi, options.inmidi)
    midiNode.init()
    # message = ZstMethod("note", "none", ZstMethod.WRITE, {"velocity":100, "note":64})
    # midiNode.play_note(message)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        midiNode.close()

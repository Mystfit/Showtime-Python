try:
    import rtmidi_python as rtmidi
except ImportError:
    import rtmidi
import platform


class MidiRouter:

    NOTE_ON = 0x90
    NOTE_OFF = 0x80

    MIDI_IN = "in"
    MIDI_OUT = "out"

    def __init__(self, midiPortIn=-1, midiPortOut=-1):
        # Setup midi port 
        self.midi_out = None
        self.midi_in = None

        if midiPortOut > -1:
            self.midi_out = self.createMidi(midiportindex, MIDI_OUT)

        if midiPortIn > -1:
            self.midi_in = self.createMidi(midiportindex, MIDI_IN)

        # Note tracking
        self.activeNotes = {}
        self.lastNote = None
        self.isMonophonic = True


    def midiOutActive(self):
        if self.midi_out:
            return True
        return False

    def midiInActive(self):
        if self.midi_in:
            return True
        return False

    def createMidi(self, midiportindex=-1, porttype):
        # Midi startup. Try creating a virtual port. Doesn't work on Windows
        midi = None
        if porttype == MIDI_IN:
            midi = rtmidi.MidiOut()
        elif porttype == MIDI_OUT:
            midi = rtmidi.MidiIn()
        else
            return None

        if midiportindex:
            if midiportindex < 0:
                if platform.system() == "Windows":
                    print "\nCan't open virtual midi port on windows. Try using loopMidi."
                	return None
                else:
                    midi.open_virtual_port("Showtime-Midi-" + porttype)
            else:
                midi.open_port(midiportindex)

        return midi


    def listMidiOutPorts(self):
        print("Available Midi Out ports:")
        portindex = 0
        for port in self.midi_out.ports:
            print str(portindex) + ": " + str(port)
            portindex += 1

    def listMidiInPorts(self):
        print("Available Midi In ports:")
        portindex = 0
        for port in self.midi_in.ports:
            print str(portindex) + ": " + str(port)
            portindex += 1

    def play_midi_note(self, message):
        trigger = MidiRouter.NOTE_ON
        velocity = int(message.args["velocity"])
        note = int(message.args["note"])

        if note in self.activeNotes:
            if self.activeNotes[note]:
                trigger = MidiRouter.NOTE_OFF
                self.activeNotes[note] = False
                velocity = 0
            else:
                self.activeNotes[note] = True

        if self.midi_out:
            if self.lastNote and self.isMonophonic and self.lastNote != note:
                self.activeNotes[note] = False
                self.midi_out.send_message([MidiRouter.NOTE_OFF, self.lastNote, 0])

            self.lastNote = note
            self.midi_out.send_message([trigger, int(message.args["note"]), velocity])

#!/usr/bin/env python
import sys
import math
import time
from Showtime.zst_node import *
import test_base

# Convert Python inputs
if sys.version[0] == "3":
    raw_input = input


class SineWave(object):

    def __init__(self, name, address):
        self.counter = 0
        self.speed = 10

        self.node = ZstNode(name, address)
        self.node.start()
        self.node.request_register_node(self.node.stage)
        self.node.request_register_method("sinewave", ZstMethod.READ)
        self.node.request_register_method(
            "set_speed", ZstMethod.WRITE, {"speed": self.speed}, self.set_speed)

    def set_speed(self, message):
        print("CHANGING SPEED")
        self.speed = message["args"]["speed"]

    def sinewave(self):
        outSine = math.sin(self.counter)
        self.counter += 1
        return self.node.update_local_method_by_name("sinewave", outSine)


if len(sys.argv) < 2:
    print("Need a stage address!")
    sys.exit(1)

sinwave = SineWave("SineWaveGenerator", sys.argv[1])

try:
    while True:
        time.sleep(1. / sinwave.speed)
        print(sinwave.sinewave())
except KeyboardInterrupt:
    sinwave.node.close()

#!/usr/bin/env python
from Showtime.zst_stage import ZstStage
import time

stage = ZstStage()
stage.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    stage.close()

print("Finished")

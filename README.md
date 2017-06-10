# IR Distance Module

This module provides a class that reads the Sharp GP2D02 infra red distance sensors on
a Raspberry Pi. It uses the GPIO daemon _pigpio_ found at http://abyz.co.uk/rpi/pigpio/

## usage example

``` python
import time
from ir_distance import IRDistance

ir = IRDistance()

ir.start()

while True:
  print ir.get_distance()
  time.

ir.stop()
`

"""
Blink the built-in LED.
Blocking.
"""

import time
from adafruit_circuitplayground import cp

cp.red_led = False;

while True:
    cp.red_led = True
    time.sleep( 0.5 )
    cp.red_led = False
    time.sleep( 0.5 )

"""
Blink the built-in LED.
Blocking.
"""

# libraries
import time
from adafruit_circuitplayground import cp

# setup
cp.red_led = False;

print("blink LED")

# loop
while True:
    cp.red_led = True
    time.sleep( 0.5 )
    cp.red_led = False
    time.sleep( 0.5 )

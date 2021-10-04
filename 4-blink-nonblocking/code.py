"""
Blink built-in led and neo-pixel.
Non-blocking.
"""

# libraries
import time
from adafruit_circuitplayground import cp
from every.every import Every

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

# setup
# periodics
blink_led = Every(0.150) # in seconds
blink_neo = Every(0.500)

cp.red_led = False
cp.pixels.brightness = 0.05 # 0.0 to 1.0
cp.pixels[ 1 ] = OFF

print("blink non-blocking")

# loop
while True:

    if blink_led():
        cp.red_led = not cp.red_led

    if blink_neo():
        if cp.pixels[ 1 ] == OFF:
            cp.pixels[ 1 ] = LIGHT_COLOR
        else:
            cp.pixels[ 1 ] = OFF

    time.sleep(0.001) # allow reload

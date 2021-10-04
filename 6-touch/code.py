"""
Respond to a touch on A1
"""

# libraries
import time
from every.every import Every
from adafruit_circuitplayground import cp

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

# set up
# no setup for "touch"
heartbeat = Every(1)
cp.pixels.brightness = 0.05 # 0.0 to 1.0
cp.pixels[ 1 ] = OFF

print("touch a1")

# loop
while True:
    if cp.touch_A1:
        cp.pixels[ 1 ] = LIGHT_COLOR
    else:
        cp.pixels[ 1 ] = OFF

    # look alive
    if heartbeat():
        cp.red_led = not cp.red_led

    time.sleep(0.001) # allow reload

"""
Respond to a touch on A1 & A2
"""

# libraries
import time
from every.every import Timer
from adafruit_circuitplayground import cp

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )
automatic = Timer(8)
automatic.start() # need to start initially
on_duration = Timer(1)

# set up
# no setup for "touch"
cp.pixels.brightness = 0.05 # 0.0 to 1.0
cp.pixels[ 1 ] = OFF

print("touch a1 & a2")

# loop
while True:
    if cp.touch_A1 and cp.touch_A2:
        cp.pixels[ 1 ] = LIGHT_COLOR
        automatic.start()

    elif cp.touch_A3 or cp.touch_A4:
        cp.pixels[ 1 ] = LIGHT_COLOR
        automatic.start()
    
    elif automatic():
        cp.pixels[ 1 ] = LIGHT_COLOR
        on_duration.start()
        print("auto")

    elif on_duration.running:
        on_duration() # won't expire otherwise
        
    else:
        cp.pixels[ 1 ] = OFF

    # slow the loop so we can upload
    time.sleep( 0.01 )

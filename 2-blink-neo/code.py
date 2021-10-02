"""
Blink a neo-pixel.
Blocking.
"""

# libraries
import time
from adafruit_circuitplayground import cp

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

# setup
cp.pixels.brightness = 0.6 # 0.0 to 1.0

# loop
while True:
    cp.pixels[ 1 ] = LIGHT_COLOR
    time.sleep( 0.5 )
    cp.pixels[ 1 ] = OFF
    time.sleep( 0.5 )

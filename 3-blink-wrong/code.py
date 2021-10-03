"""
Blink built-in led and neo-pixel.
Blocking.
"""

# libraries
import time
from adafruit_circuitplayground import cp

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

# setup
cp.red_led = False;
cp.pixels.brightness = 0.05 # 0.0 to 1.0

print("blink blocking")

# loop
while True:
    # "copypasta" of blink & blink-neo

    cp.red_led = True
    time.sleep( 0.5 )
    cp.red_led = False
    time.sleep( 0.5 )

    cp.pixels[ 1 ] = LIGHT_COLOR
    time.sleep( 0.5 )
    cp.pixels[ 1 ] = OFF
    time.sleep( 0.5 )

"""
Respond to a touch
"""

# libraries
from adafruit_circuitplayground import cp

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

# set up
# no setup for "touch"
cp.pixels.brightness = 0.6 # 0.0 to 1.0
cp.pixels[ 1 ] = OFF

# loop
while True:
    if cp.touch_A1:
        print( "A1 touched" )
        cp.pixels[ 1 ] = LIGHT_COLOR

    else:
        print( "A1 release" )
        cp.pixels[ 1 ] = OFF

    # slow the loop so we can upload
    time.sleep( 0.01 )

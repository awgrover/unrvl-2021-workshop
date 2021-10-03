"""
Respond to a switch
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

d1 = digitalio.DigitalInOut(board.D1)
d1.switch_to_output()

on s1, light neo & external 1
on s2 for 1 second

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

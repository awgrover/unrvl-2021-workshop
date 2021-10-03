"""
Respond to a switch
"""

# libraries
from adafruit_circuitplayground import cp
from every.every import Timer

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

# set up
# no setup for "touch"
cp.pixels.brightness = 0.05 # 0.0 to 1.0
cp.pixels[ 1 ] = OFF

led1 = digitalio.DigitalInOut(board.A0)
led1.switch_to_output()

on s1, light neo & external 1
on s2 for 1 second

# loop
while True:
    if cp.touch_A1:
        cp.pixels[ 1 ] = LIGHT_COLOR

    else:
        cp.pixels[ 1 ] = OFF

    # slow the loop so we can upload
    time.sleep( 0.01 )

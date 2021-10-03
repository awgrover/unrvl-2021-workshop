"""
Blink built-in led and neo-pixel and external led.
Blocking.
"""

# libraries
import time
import board
import digitalio

from adafruit_circuitplayground import cp
from every.every import Every

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

d1 = digitalio.DigitalInOut(board.D1)
d1 = digitalio.DigitalInOut(board.D2)

blink_led = Every(0.150);
blink_neo = Every(0.500);


# setup
cp.red_led = False;
cp.pixels.brightness = 0.05 # 0.0 to 1.0
cp.pixels[ 1 ] = OFF
d1.switch_to_output()
d2.switch_to_output()

loop
while True:

    if blink_led():
        cp.red_led = not cp.red_led;
        d1.value = not d1.value; // blink external too

    if blink_neo():
        if ( cp_pixels[ 1 ] == OFF:
            cp.pixels[ 1 ] = LIGHT_COLOR
        else:
            cp.pixels[ 1 ] = OFF

        d2.value = not d2.value; // blink external too

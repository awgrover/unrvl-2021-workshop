"""
Blink built-in led and neo-pixel and external led.
Non-blocking.
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

# setup
led1 = digitalio.DigitalInOut(board.A1)
led2 = digitalio.DigitalInOut(board.A2)

blink_led = Every(0.150)
blink_neo = Every(0.500)

cp.red_led = False
cp.pixels.brightness = 0.05 # 0.0 to 1.0
cp.pixels[ 1 ] = OFF
led1.switch_to_output()
led2.switch_to_output()

print("blink w/external")

# loop
while True:

    if blink_led():
        # "state" is in cp.red_led, and led1.value (true/false)
        cp.red_led = not cp.red_led
        led1.value = not led1.value # blink external too

    if blink_neo():
        # "state" is the last color
        if cp.pixels[ 1 ] == OFF:
            cp.pixels[ 1 ] = LIGHT_COLOR
        else:
            cp.pixels[ 1 ] = OFF

        led2.value = not led2.value # blink external too

    time.sleep(0.001) # allow reload

"""
Respond to a switch
"""

# libraries
import board
import digitalio
import time
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

button1 = digitalio.DigitalInOut(board.A2)
button1.switch_to_input(pull=digitalio.Pull.UP) # "open" is True

button2 = digitalio.DigitalInOut(board.A3)
button2.switch_to_input(pull=digitalio.Pull.UP) # "open" is True

on_duration_expired = Timer(1.0)

print("digital control")

# loop
while True:

    # Start "still on"?
    if not button2.value:
        # closed: restart timer, i.e. "not expired"
        on_duration_expired.start()
        cp.pixels[ 1 ] = LIGHT_COLOR
        led1.value = True

    # End "still on"?
    if on_duration_expired():
        # only once (each) at end of timer
        cp.pixels[ 1 ] = OFF
        led1.value = False

    # Only concern ourselves with button1 if button2 isn't still on
    elif not on_duration_expired.running:

        if not button1.value:
            cp.pixels[ 1 ] = LIGHT_COLOR
            led1.value = True
        else:
            cp.pixels[ 1 ] = OFF
            led1.value = False

        # slow the loop so we can upload
        time.sleep( 0.01 )

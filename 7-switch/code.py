"""
Respond to an external button on A2 or A3
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

# "if x'ed...
persisted_button2 = Timer(1.0)

print("digital control")

# loop
while True:

    # Start "still on"?
    # "closed" gives false, "open" gives true
    if not button2.value:
        # restart timer, i.e. "persist till"
        persisted_button2.start()
        cp.pixels[ 1 ] = LIGHT_COLOR
        led1.value = True

    # End of "still on"?
    # only once (each) at end of timer
    if persisted_button2():
        cp.pixels[ 1 ] = OFF
        led1.value = False

    # Only concern ourselves with button1 if button2 isn't still on
    # Because we use the same neo-pixel
    elif not persisted_button2.running:

        if not button1.value:
            cp.pixels[ 1 ] = LIGHT_COLOR
            led1.value = True
        else:
            cp.pixels[ 1 ] = OFF
            led1.value = False

    time.sleep(0.001) # allow reload

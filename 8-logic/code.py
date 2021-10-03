"""
Variations on reacting to inputs.

Inputs:

Touch A1: react
Pressure/Resistance A0: brightness, react
Digital A2: react
Digital A3: react after a delay
Digital A4: react sometimes
Periodically: react if nothing else recently

Outputs:

Neopixel 0: brightness
Neopixel 1: act
Digital Pad A5: act
Digital Pad A6/A7: alternating react 

Modifiers:

"""

# libraries
import board
import digitalio
import time
import analogio
import random
from adafruit_circuitplayground import cp
from every.every import Timer
from every.every import Every

# globals
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
PRESSURE_COLOR = ( 0,0,255 )
OFF = ( 0, 0, 0 )
MINIMUM_BRIGHTNESS = 0.01 # 0.0 to 1.0

# set up
# no setup for "touch"
cp.pixels.brightness = MINIMUM_BRIGHTNESS
cp.pixels[ 0 ] = PRESSURE_COLOR
# name our neo's by the pad they are near
neoA5 = cp.pixels[ 1 ] 
neoA5 = OFF
neoA6 = cp.pixels[ 3 ] 
neoA6 = OFF
neoA7 = cp.pixels[ 4 ] 
neoA7 = OFF

plain_out = digitalio.DigitalInOut(board.A5)
plain_out.switch_to_output()
alt1_out = digitalio.DigitalInOut(board.A6)
alt1_out.switch_to_output()
alt2_out = digitalio.DigitalInOut(board.A7)
alt2_out.switch_to_output()
alt_selector = False # just alternate

pressure = analogio.AnalogIn(board.A0)
PRESSURE_ON = 4000 # test and find

button1 = digitalio.DigitalInOut(board.A2)
button1.switch_to_input(pull=digitalio.Pull.UP) # "open" is True

button2 = digitalio.DigitalInOut(board.A3)
button2.switch_to_input(pull=digitalio.Pull.UP) # "open" is True

duration = Timer(1.0)
attractor = Timer(random.uniform(4.0, 6.0))
attractor.start()

class Modes:
    # A list of things we could be doing
    # see `mode` variable
    NULL = -1 # not used
    IDLE = 0 # not doing anything else
    ONCE = 1
    TOUCHA1 = 2
    PRESSURE = 3

mode = Modes.IDLE # what are we doing?
was_mode = Modes.NULL

# Functions
def act_on():
    global alt_selector

    neoA5 = LIGHT_COLOR
    plain_out.value = True

    if alt_selector:
        alt1_out.value = True
    elif alt_selector:
        alt2_out.value = True
    alt_selector = not alt_selector

def act_off():
    neoA5 = OFF
    plain_out.value = False

    # don't need to check alt_selector
    alt1_out.value = False
    alt2_out.value = False

was_pressure = 0
def track():
    # things that constantly keep track
    raw = pressure.value / 65535.0 # convert to 0 .. 1.0
    cp.brightness = max(MINIMUM_BRIGHTNESS, raw) # keep minimum
    if raw != was_pressure:
        print("P ",raw)
        was_pressure = raw

print("logic")

# loop
while True:
    
    # only consider new inputs if we are idle
    if mode == Modes.IDLE:

        if cp.touch_A1:
            act_on()
            mode = Modes.TOUCHA1

        elif pressure.value > PRESSURE_ON:
            act_on()
            mode = Modes.PRESSURE
            print(pressure.value)

        elif attractor():
            act_on()
            mode = Modes.ONCE
            duration.start()

    elif mode == Modes.TOUCHA1:
        # wait for un-touch
        if not cp.touch_A1:
            act_off()
            mode = Modes.IDLE

    elif mode == Modes.ONCE:
        if duration():
            act_off()
            mode = Modes.IDLE

    elif mode == Modes.PRESSURE:
        if pressure.value < PRESSURE_ON: # ha! "1" hysteresis
            act_off()
            mode = Modes.IDLE

    # doing something:
    if mode != Modes.IDLE:
        # if we are doing something, reset time-till-attractor
        attractor.start()

    # debugging, watch things change
    if mode != was_mode:
        print(was_mode," -> ", mode);
        was_mode = mode

    time.sleep( 0.01 )
"""
    # Start "still on"?
    if not button2.value:
        # closed: restart timer, i.e. "not expired"
        on_duration_expired.start()
        neoA5 = LIGHT_COLOR
        led1.value = True

    # End "still on"?
    if on_duration_expired():
        # only once (each) at end of timer
        neoA5 = OFF
        led1.value = False

    # Only concern ourselves with button1 if button2 isn't still on
    elif not on_duration_expired.running:

        if not button1.value:
            neoA5 = LIGHT_COLOR
            led1.value = True
        else:
            neoA5 = OFF
            led1.value = False

        # slow the loop so we can upload
        time.sleep( 0.01 )
"""

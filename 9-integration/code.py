"""
    Variations on reacting to inputs.

    Inputs:

    Touch A1: react
    Pressure/Resistance A2: brightness, react
    Digital A3: react after a delay
    Digital A4: react sometimes
    Periodically: react if nothing else recently

    Outputs:

    Neopixel 2: brightness
    Neopixel 1,3,4: act
    Neopixels near inputs: flash green on input
    Digital Pad A5: act
    Digital Pad A6/A7: alternating react 

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

# globals & setup
LIGHT_COLOR = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
PRESSURE_COLOR = ( 0,0,255 )
INPUT_COLOR = (0,255,0)
OFF = ( 0, 0, 0 )
MINIMUM_BRIGHTNESS = 0.01 # 0.0 to 1.0
# name our neo's by the pad they are near
neoA0 = 5
neoA1 = 6
neoA2 = 8
neoA3 = 9
neoA4 = 0
neoA5 = 1
neoA6 = 3
neoA7 = 4
PRESSURE_ON = 5000 # test and find
SOMETIMES_RATE = 0.8 # aka "damping"
flash = None

# no setup for "touch"
cp.pixels.brightness = MINIMUM_BRIGHTNESS
cp.pixels[ 2 ] = PRESSURE_COLOR

plain_out = digitalio.DigitalInOut(board.A5)
plain_out.switch_to_output()
alt1_out = digitalio.DigitalInOut(board.A6)
alt1_out.switch_to_output()
alt2_out = digitalio.DigitalInOut(board.TX)
alt2_out.switch_to_output()
alt_selector = False # just alternate

pressure = analogio.AnalogIn(board.A2) # a1..a6 on ble

delay_in = digitalio.DigitalInOut(board.A3)
delay_in.switch_to_input(pull=digitalio.Pull.UP) # "open" is True
delay_action = Timer(0.75) # delayed action

sometimes_in = digitalio.DigitalInOut(board.A4)
sometimes_in.switch_to_input(pull=digitalio.Pull.UP) # "open" is True

duration = Timer(1.0)
attractor = Timer(random.uniform(4.0, 6.0))
attractor.start() # needs to start initially

input_flashing = Timer(0.1)

class Modes:
    # A list of things we could be doing
    # see `mode` variable
    IDLE = 0 # not doing anything else
    ONCE = 1
    TOUCHA1 = 2
    PRESSURE = 3
    DELAY_ONCE = 5
    SOMETIMES_BUTTON = 6


mode = Modes.IDLE # what are we doing?
was_mode = None

# Functions
def act_on():
    global alt_selector

    cp.pixels[ neoA5 ] = LIGHT_COLOR
    plain_out.value = True

    # choose which alternating output
    if alt_selector:
        alt1_out.value = True
        cp.pixels[ neoA6 ] = LIGHT_COLOR
    else:
        alt2_out.value = True
        cp.pixels[ neoA7 ] = LIGHT_COLOR
    alt_selector = not alt_selector

def act_off():
    cp.pixels[ neoA5 ] = OFF
    plain_out.value = False

    # don't need to check alt_selector
    alt1_out.value = False
    alt2_out.value = False
    cp.pixels[ neoA6 ] = OFF
    cp.pixels[ neoA7 ] = OFF

was_pressure = 0
def track():
    global was_pressure
    # things that constantly keep track
    raw = pressure.value / 65535.0 # convert to 0 .. 1.0
    cp.pixels.brightness = max(MINIMUM_BRIGHTNESS, raw) # keep minimum
    if raw != was_pressure:
        # print("P ",raw, " B ",cp.pixels.brightness) # uncomment for tracking pressure
        was_pressure = raw

print("logic")

# loop
while True:
    
    # only consider new inputs if we are idle
    if mode == Modes.IDLE:

        if cp.touch_A1:
            act_on()
            flash = neoA1
            mode = Modes.TOUCHA1

        elif pressure.value > PRESSURE_ON:
            act_on()
            mode = Modes.PRESSURE
            flash = neoA0
            print(pressure.value)

        elif attractor():
            act_on()
            mode = Modes.ONCE
            duration.start()
        
        # digital in "buttons"
        # open = True, closed = False
        
        elif not delay_in.value:
            # wait for it...
            flash = neoA3
            mode = Modes.DELAY_ONCE
            delay_action.start()

        elif not sometimes_in.value:
            if random.random() >= SOMETIMES_RATE:
                act_on()
                flash = neoA4
                mode = Modes.SOMETIMES_BUTTON

    elif mode == Modes.TOUCHA1:
        # wait till un-touch
        if not cp.touch_A1: # not AUDIO
            act_off()
            mode = Modes.IDLE

    elif mode == Modes.ONCE:
        if duration():
            act_off()
            mode = Modes.IDLE

    elif mode == Modes.PRESSURE:
        # wait till "un" pressure
        if pressure.value < (PRESSURE_ON * 0.9): # ha! hysteresis
            act_off()

    elif mode == Modes.DELAY_ONCE:
        # waiting for delayed action
        if delay_action():
            act_on()
            duration.start()
            # continue on for "ONCE" duration
            mode = Modes.ONCE 

    elif mode == Modes.SOMETIMES_BUTTON:
        # wait till "open"
        if sometimes_in.value:
            act_off()
            mode = Modes.IDLE

    # signal an input by flashing the neo near the pin
    if flash:
        if not input_flashing.running:
            cp.pixels[ flash ] = INPUT_COLOR
            input_flashing.start()
        elif input_flashing():
            cp.pixels[ flash ] = OFF
            flash = None

    # doing something:
    if mode != Modes.IDLE:
        # if we are doing something, reset time-till-attractor
        attractor.start()

    track()

    # debugging, watch things change
    if mode != was_mode:
        print(was_mode," -> ", mode)
        was_mode = mode

    time.sleep(0.001) # allow reload

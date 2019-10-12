#!/usr/bin/env python3
# NOTE: change to micropython for optimized performance (but no sounds)
'''example scripts that you can copy to your own files'''

import os
import sys
import time
import random
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor

def turn(direction, degrees):

    left_speed = 0
    right_speed = 0
    speed = 50

    if direction == LEFT:
        left_speed = -speed
        right_speed = speed
    elif direction == RIGHT:
        left_speed = speed
        right_speed = -speed

    mt.on_for_degrees(left_speed, right_speed, degrees * 4)

def turn_2(direction, degrees):

    left_speed = 0
    right_speed = 0
    speed = 50

    if direction == LEFT:
        left_speed = -speed
        right_speed = speed
    elif direction == RIGHT:
        left_speed = speed
        right_speed = -speed

    mt.on_for_seconds(left_speed, right_speed, degrees / 85)

btn = Button()

# lets keep this on top of the file for easy editing
def main():
    '''The main function of our program'''

    setup_brick_console()
    battery_check()

    mt = MoveTank(OUTPUT_D, OUTPUT_A) # control the two motors at once
    # drive motor in A port at 50 % max speed, motor in port B at 75% max speed for 10 seconds
    mt.on_for_seconds(-75, 0, 2)
    # mt.follow_line

    # print color sensor input to the brick:
    # cs = ColorSensor(INPUT_1)
    #while True:
     #   print(cs.color_name)
     #  time.sleep(0.01)

    # irs = InfraredSensor(INPUT_1)
'''
    # while True:
        if irs.proximity < 40 * 1.4:
            print("less than 40!")
        else:
            print("too far away!") '''
'''
    # wait for left button press
    while True:
        btn.wait_for_bump('left', timeout_ms=300)
        # on_button_press()
        time.sleep(0.01) # give the processor time to 'rest' between button checks '''

    # print something to the output panel in VS Code
    # debug_print('Hello VS Code!')

    # wait a bit so you have time to look at the display before the program
    # exits
    # time.sleep(3)

# XXXXXXXXXXXXXXXXXXX METHODS XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# def on_button_press():
    # do stuff

def setup_brick_console():
    '''Make the device console (screen) more legible'''
    os.system('setfont ' + 'Lat15-Terminus24x12')
    print('\x1Bc', end='') # reset console
    print('\x1B[?25l', end='') # disable the cursor

def battery_check():
    '''Warns us of low battery with a beep and a sound msg.'''
    voltage = PowerSupply().measured_volts
    if voltage < LOW_BATTERY_VOLTAGE_THRESHOLD:
        play_beep(400.0, 2.0) # Hz; seconds
        Sound().speak('Warning! Battery running low!')
    elif voltage < MIDDLE_VOLTAGE_THRESHOLD:
        play_beep(length=2.0)
        Sound().speak('Battery at midway point.')
    print(voltage)

# this seems useful, so it should be preserved
def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.'''
    print(*args, **kwargs, file=sys.stderr)

def play_beep(hz=300.0, length=1.0):
    Sound().play_tone(hz, length)

# XXXXXXXXXXXXXXXXXXX STATIC CONSTANTS ETC XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# state constants
ON = True
OFF = False

# supposedly, the battery runs out very quickly after 5 volts
LOW_BATTERY_VOLTAGE_THRESHOLD = 5.0

MIDDLE_VOLTAGE_THRESHOLD = 7.0

# not sure if this is needed; let's keep it for now
if __name__ == '__main__':
    main()

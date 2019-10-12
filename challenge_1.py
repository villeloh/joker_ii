#!/usr/bin/env python3

'''1 THE CACHE
Find your way through the maze-like server room holding all the information
needed to run the autonomous facility. You’ll probably need to trigger
maintenance mode to pass though!
Bonus points
- Beat the maze under 20 seconds +5p'''

import os
import sys
import time
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_B, MediumMotor, MoveTank
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor

btn = Button()

mt = MoveTank(OUTPUT_D, OUTPUT_A)

mm = MediumMotor(OUTPUT_B)

cs = ColorSensor(INPUT_3)

irs = InfraredSensor(INPUT_2)

def main():

    setup_brick_console()
    battery_check()
    play_beep()

    irs.on_channel1_top_left = top_left_channel_1_action
    irs.on_channel1_top_right = top_right_channel_1_action

    while True:
        irs.process()
        time.sleep(0.01)

'''
    while True:
        play_beep()
        btn.wait_for_bump('enter', timeout_ms=300)
        run_script() '''

def run_script():
    while cs.color_name != 'White':
        mt.on_for_seconds(50, 50, 0.3, block = False)

    play_beep(length=0.1)
    follow_line(mt, 30, 'White')
    # mt.follow_line(kp=11.3, ki=0.05, kd=3.2, speed=SpeedPercent(30), follow_for='follow_for_ms', ms=1000)

    while True:
        # print(cs.color_name)
        # print(cs.rgb)
        if (cs.color_name == 'White'):
            print(cs.color_name)
        else:
            print('Non-White')
            # mt.off()
            # play_beep()
            # n = 1
        time.sleep(0.01)

def follow_line(mt, speed, color_name):
    turning_right = True
    right_angle = False
    while True:
        if cs.color_name == color_name:
            mt.on_for_seconds(speed, speed, 0.2, block = False)
        elif turning_right:
            mt.on_for_seconds(-speed, speed, 0.1, block = False)
            turning_right = False
        else:
            mt.on_for_seconds(speed, -speed, 0.1, block = False)
            turning_right = True
            right_angle = True
        if right_angle:
            mt.on_for_seconds(-speed, speed, 0.5, block = False)
            right_angle = False
            if cs.color_name == color_name:
                 mt.on_for_seconds(speed, -speed, 0.5, block = False)

def top_left_channel_1_action(state):
    if state:
        run_script()

def top_right_channel_1_action(state):
    if state:
        mm.on_for_degrees(30, -360, block = False)

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

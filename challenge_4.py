#!/usr/bin/env micropython

'''4 THE ROOT
A chamber of massive steel pillars holding up the Monolith computing grounds.
Find your way through!
Bonus points
- Use a top-down camera and Computer Vision to find a way through +5p'''

import os
import sys
import time
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.button import Button
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent

mt = MoveTank(OUTPUT_A, OUTPUT_D)
irs = InfraredSensor(INPUT_2)

LEFT = 'LEFT'
RIGHT = 'RIGHT'

def main():

    setup_brick_console()
    battery_check()
    play_beep()

    irs.on_channel1_top_left = top_left_channel_1_action

    while True:
        irs.process()
        time.sleep(0.01)

def top_left_channel_1_action(state):
    if state:
        straight_ahead(50, 1)
        turn(LEFT, 90)
        straight_ahead(50, 4)
        turn(RIGHT, 90)
        straight_ahead(50, 6)
        turn(RIGHT, 90)

def straight_ahead(speed, seconds):
    mt.on_for_seconds(speed, speed, seconds)

def turn_unfinished_do_not_use(direction, degrees):

    left_speed = 0
    right_speed = 0
    speed = 50

    if direction == LEFT:
        left_speed = -speed
        right_speed = speed
    elif direction == RIGHT:
        left_speed = speed
        right_speed = 0

    mt.on_for_degrees(left_speed, right_speed, degrees * 4)

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

    mt.on_for_seconds(left_speed, right_speed, degrees / 103)

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

def play_beep(hz=300.0, length=3.0):
    Sound().play_tone(hz, length)

# XXXXXXXXXXXXXXXXXXX STATIC CONSTANTS ETC XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# supposedly, the battery runs out very quickly after 5 volts
LOW_BATTERY_VOLTAGE_THRESHOLD = 5.0

MIDDLE_VOLTAGE_THRESHOLD = 7.0

# not sure if this is needed; let's keep it for now
if __name__ == '__main__':
    main()

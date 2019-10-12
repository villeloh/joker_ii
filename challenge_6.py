#!/usr/bin/env python3

'''6 THE TERMINAL
The main maintenance terminal, last used in Monolith’s installation years ago.
Theoretically, this should allow you to bypass the automated maintenance and
facility isolation security principles, making it possible to connect to outside
networks. You are not the only one who wants access!
Bonus points
- Successfully deliver USB payload (insert device) +10p
- Have the high ground! (Win a match) +5p
There are 6 slots on the platform. If you arrive among the first, you may park your
robot in a vacant slot.
When the slots are full, or if you wish to do so before, you’ll need to challenge one
of the slot holders to a battle.
A robot that falls off the platform is defeated and will have to exit the TERMINAL.'''

import os
import sys
import time
import random
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.button import Button
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent

mt = MoveTank(OUTPUT_A, OUTPUT_D)
irs = InfraredSensor(INPUT_2)
cs = ColorSensor(INPUT_3)

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

def sweeping_turn(direction):
    if direction == LEFT:
        mt.on_for_seconds(40, 80, 2, block=False)
    elif direction == RIGHT:
        mt.on_for_seconds(80, 40, 2, block=False)

def run_fight_logic():
    while True:
        if (random.choice([LEFT, RIGHT]) == LEFT):
            sweeping_turn(LEFT)
        else:
            sweeping_turn(RIGHT)

        # to prevent it from calling the sweeping_turn over
        # and over again (without blocking, which also disables the color sensor)
        countDown = 300000
        while (countDown > 0):
            countDown = countDown - 1
            if (cs.color_name == 'NoColor'):
                straight_reverse(70, 1)
                return
        time.sleep(0.01)

def top_left_channel_1_action(state):
    if state:
        straight_ahead(50, 1)
        run_fight_logic()

def straight_ahead(speed, seconds):
    mt.on_for_seconds(speed, speed, seconds)

def straight_reverse(speed, seconds):
    mt.on_for_seconds(-speed, -speed, seconds)

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

    mt.on_for_seconds(left_speed, right_speed, degrees / 103, block=False)

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

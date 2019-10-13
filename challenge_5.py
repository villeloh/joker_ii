#!/usr/bin/env python3

'''5 TRI-CENTRIFUGE
A line of massive centrifuges used to conduct material research before the
incident. Watch out for broken shards of test equipment!
Bonus points
- Do not hit any walls! +5p'''

import os
import sys
import time
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.button import Button
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor , TouchSensor
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveTank
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM, SpeedPercent

mt = MoveTank(OUTPUT_A, OUTPUT_D)
irs = InfraredSensor(INPUT_2)
cs = ColorSensor(INPUT_3) # not used atm
ts = TouchSensor(INPUT_1)

LEFT = 'LEFT'
RIGHT = 'RIGHT'

def moveback() :
    mt.on_for_seconds(-45,-45 , 0.5)

def touched() :
    if ts.is_pressed :
        moveback()

def main():

    setup_brick_console()
    battery_check()
    play_beep()

    irs.on_channel1_top_left = top_left_channel_1_action
    irs.on_channel1_top_right = top_right_channel_1_action
    irs.on_channel1_bottom_left = bottom_left_channel_1_action
    irs.on_channel1_bottom_right = bottom_right_channel_1_action

    while True:
        irs.process()
        time.sleep(0.01)

def sweeping_turn(direction, seconds):
    if direction == LEFT:
        mt.on_for_seconds(40, 70, seconds)
    elif direction == RIGHT:
        mt.on_for_seconds(70, 40, seconds)

#def check_hole()

def Off_WhenWalls(dir) :
     if not irs.proximity  < 15 * 1.4  :

        while not irs.proximity  < 15 * 1.4 :
                straight_ahead(90,0.8)
                if irs.proximity  < 15 * 1.4 :
                    #play_beep(length=3)
                    moveback()
                    time.sleep(2)
                sweeping_turn(dir, 1)
                dir = TriggerWhite()

        #play_beep(length=3)
        time.sleep(0.01)
        while irs.proximity  < 15 * 1.4 :
            if not irs.proximity  < 15 * 1.4 :
                touched()
                straight_ahead(90,0.8)


def top_left_channel_1_action(state):

    if state:
        # straight_ahead(90, 3)
        dir = TriggerWhite()
        sweeping_turn(LEFT, 3)


    if not irs.proximity  < 15 * 1.4  :

        while not irs.proximity  < 15 * 1.4 :
                touched()
                straight_ahead(90,0.8)
                if irs.proximity  < 15 * 1.4 :
                    #play_beep(length=3)
                    moveback()
                    time.sleep(2)
                sweeping_turn(dir, 1)
                dir = TriggerWhite()
                #sweeping_turn(dir, 3)
        #play_beep(length=3)
        time.sleep(0.01)
        while irs.proximity  < 15 * 1.4 :
            if not irs.proximity  < 15 * 1.4 :
                touched()
                straight_ahead(90,0.8)
    Off_WhenWalls(dir)

def top_right_channel_1_action(state):
    if state:
        # straight_ahead(90, 3)
        sweeping_turn(LEFT, 4)

        firstMove = False
        secondMove = False

        while not firstMove:
            if irs.proximity * 0.7 > 60:
                straight_ahead(90, 3)
                #play_beep(length=1)
                firstMove = True
            time.sleep(0.01)
        while not secondMove:
            if irs.proximity * 0.7 > 60:
                straight_ahead(90, 3)
                #play_beep(length=3)
                secondMove = True
            time.sleep(0.01)

def bottom_right_channel_1_action(state):
    if state:
        # straight_ahead(90, 3)
        sweeping_turn(LEFT, 5)

        firstMove = False
        secondMove = False

        while not firstMove:
            if irs.proximity * 0.7 > 60:
                straight_ahead(90, 3)
                firstMove = True
                #play_beep(length=3)
            time.sleep(0.01)
        while not secondMove:
            if irs.proximity * 0.7 > 60:
                straight_ahead(90, 3)
                #play_beep(length=3)
                secondMove = True
            time.sleep(0.01)

def bottom_left_channel_1_action(state):
        if state:
            straight_ahead(90, 3)
            time.sleep(7.5)
            reverse(90, 3)
            time.sleep(12)
            straight_ahead(90, 3)
            # continue to the other gate



def straight_ahead(speed, seconds):
    mt.on_for_seconds(speed, speed, seconds)

def reverse(speed, seconds):
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

def TriggerWhite() :
    direction = 'LEFT'
    changeCount = 0
    if cs.color_name == 'White':
        if changeCount == 0 :
            changeCount = changeCount + 1
            direction = 'LEFT'
            play_beep(length=2.0)
        if changeCount == 1 :
            changeCount = changeCount - 1
            direction = 'RIGHT'
            play_beep(length=2.0)
    return direction

if __name__ == '__main__':
    main()

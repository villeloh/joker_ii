#!/usr/bin/env python3
# NOTE: change to micropython for optimized performance (but no sounds)
'''Just testing things out'''

import os
import sys
import time
import random
from ev3dev2.sound import Sound
from ev3dev2.power import PowerSupply
from ev3dev2.button import Button
from ev3dev2.motor import OUTPUT_A, OUTPUT_D, OUTPUT_B, MoveTank, MediumMotor
from ev3dev2.motor import SpeedDPS, SpeedRPM, SpeedRPS, SpeedDPM
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, InfraredSensor

btn = Button()
mt = MoveTank(OUTPUT_A, OUTPUT_D)
irs = InfraredSensor(INPUT_2)
mm = MediumMotor(OUTPUT_B)

states = [0,0,0,0] # top left, top right, bottom left, bottom right

def top_left_channel_1_action(state):
    states[0]=state
    resolve_action(state)

def bottom_left_channel_1_action(state):
    states[2]=state
    resolve_action(state)

def top_right_channel_1_action(state):
    states[1]=state
    resolve_action(state)

def bottom_right_channel_1_action(state):
    states[3]=state
    resolve_action(state)

def turn_left(state):
    if state:
        mt.on(-50, 50)
    else:
        mt.off()

def turn_right(state):
    if state:
        mt.on(50, -50)
    else:
        mt.off()

def reverse(state):
    if state:
        mt.on(-80, -80)
    else:
        mt.off()

def straight_forward(state):
    if state:
        mt.on(80, 80)
    else:
        mt.off()

def clockwise_swipe(state):
    if state:
        mm.on(10)
    else:
        mm.off()

def counter_clockwise_swipe(state):
    if state:
        mm.on(-10)
    else:
        mm.off()

def resolve_action(state):
    mt.off()
    mm.off()
    if states == [1,0,0,0]: # top left button
        straight_forward(state)
    elif states == [0,0,1,0]: # reverse
        reverse(state)
    elif states == [0,1,0,0]: # top right
        turn_left(state)
    elif states == [0,0,0,1]: # bottom right
        turn_right(state)
    elif states == [1,1,0,0]: # top left & top right
        clockwise_swipe(state)
    elif states == [0,0,1,1]: # bottom left & bottom right
        counter_clockwise_swipe(state)

irs.on_channel1_top_left = top_left_channel_1_action
irs.on_channel1_top_right = top_right_channel_1_action
irs.on_channel1_bottom_left = bottom_left_channel_1_action
irs.on_channel1_bottom_right = bottom_right_channel_1_action

def main():
    '''The main function of our program'''

    setup_brick_console()
    battery_check()
    play_beep(length=2.2)

    while True:
        irs.process()
        time.sleep(0.01)

# XXXXXXXXXXXXXXXXXXX METHODS XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def on_button_press():
    play_random_quote()

def play_random_quote():
    '''A word from our sponsor, Anatoly Dyatlov'''
    index = random.randint(0, len(soundList) - 1)
    # keep moving while speaking
    Sound().speak(soundList[index], play_type=Sound.PLAY_NO_WAIT_FOR_COMPLETE)

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

def race_loss_routine():
    '''Call this in case the worst happens'''
    Sound().speak('We did everything right!', play_type=Sound.PLAY_LOOP)

# this seems useful, so it should be preserved
def debug_print(*args, **kwargs):
    '''Print debug messages to stderr.
    This shows up in the output panel in VS Code.'''
    print(*args, **kwargs, file=sys.stderr)

def play_beep(hz=300.0, length=1.0):
    Sound().play_tone(hz, length)

# XXXXXXXXXXXXXXXXXXX STATIC CONSTANTS ETC XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# supposedly, the battery runs out very quickly after 5 volts
LOW_BATTERY_VOLTAGE_THRESHOLD = 5.0

MIDDLE_VOLTAGE_THRESHOLD = 7.0

soundList = [
    'Three point six rontgen. Not great, not terrible.',
    'Take him to the infirmary, he\'s delusional',
    'He\'s in shock, get him out of here!',
    'You\'re confused, RBMK reactor cores do not explode',
    'You did NOT see graphite, because it was NOT THERE!',
    'I would like to be considered',
    'We have the situation under control',
    'I was in the toilet',
    'Did you lower the control rods or not?',
    'So everything is my fault?!',
    'Do you think the right question will get you the truth?',
    'You morons blew the tank!',
    'Idiots! How the hell did you get this job?',
    'I cannot make things easier for you, but I can certainly make them harder',
    'I need WATER in my reactor core!!!',
    'The feedwater is mildly contaminated. He will be fine. I have seen worse.',
    'The Cherenkov effect. Completely normal phenomenon. Can happen with minimal radiation.'
]

# not sure if this is needed; let's keep it for now
if __name__ == '__main__':
    main()

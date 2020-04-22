#!/usr/bin/env python

import pynput
import bluetooth

class WinKeyCodes:
    """
    Enumeration class for various virtual keyboard keys on Windows.
    Reference: https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes.
    """

    '''Media keys:'''
    NEXT        = 0xb0
    PREV        = 0xb1
    STOP        = 0xb2
    PLAY_PAUSE  = 0xb3


if __name__ == '__main__':
    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        print("  {} - {}".format(addr, name))

    # TODO: Script must have a bluetooth listener. Let the phone initiate the bluetooth connection

    if False:
        play_key = pynput.keyboard.KeyCode(vk=WinKeyCodes.PLAY_PAUSE)
        virtual_keyboard = pynput.keyboard.Controller()
        virtual_keyboard.press(play_key)
        virtual_keyboard.release(play_key)

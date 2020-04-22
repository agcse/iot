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

    VOLUME_MUTE = 0xad
    VOLUME_DOWN = 0xae
    VOLUME_UP   = 0xaf

UNIQUE_HANDSHAKE_HASH = "87c53232887a3366b0ad7666fcccc9b7"  # some random hask
PROTOCOL = bluetooth.RFCOMM

if __name__ == '__main__':
    socket, client_socket = None, None
    try:
        socket = bluetooth.BluetoothSocket(proto=PROTOCOL)
        local_address = 1  # empty local address due to "single adapter" model
        print("Available port:", bluetooth.PORT_ANY)
        socket.bind(("", bluetooth.PORT_ANY))

        accepted = False
        # 1. accept a connection
        while not accepted:
            socket.listen(1)
            client_socket, address = socket.accept()
            handshake = str(client_socket.recv(1024))
            print("Received connection from", address)
            if handshake != UNIQUE_HANDSHAKE_HASH:
                print("Bad handshake")
                client_socket.close()
                continue
            accepted = (handshake == UNIQUE_HANDSHAKE_HASH)
            print("Good handshake")

        # 2. listen to commands indefinitely
        while True:
            pass

    finally:
        # close sockets after all
        if client_socket is not None:
            client_socket.close()
        if socket is not None:
            socket.close()

    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        print("  {} - {}".format(addr, name))

    if False:  # test code for virtual keyboard events
        play_key = pynput.keyboard.KeyCode(vk=WinKeyCodes.PLAY_PAUSE)
        virtual_keyboard = pynput.keyboard.Controller()
        virtual_keyboard.press(play_key)
        virtual_keyboard.release(play_key)

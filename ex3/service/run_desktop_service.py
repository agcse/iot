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


def get_code(text):
    """
    Mapper from text string to KeyCodes
    """
    get_code.codes = {
        'NEXT': WinKeyCodes.NEXT,
        'PREV': WinKeyCodes.PREV,
        'STOP': WinKeyCodes.STOP,
        'PLAY_PAUSE': WinKeyCodes.PLAY_PAUSE,

        'VOLUME_MUTE': WinKeyCodes.VOLUME_MUTE,
        'VOLUME_DOWN': WinKeyCodes.VOLUME_DOWN,
        'VOLUME_UP': WinKeyCodes.VOLUME_UP,
    }
    return get_code.codes.get(text, None)


def press_release(key_code):
    play_key = pynput.keyboard.KeyCode(vk=WinKeyCodes.PLAY_PAUSE)
    virtual_keyboard = pynput.keyboard.Controller()
    virtual_keyboard.press(play_key)
    virtual_keyboard.release(play_key)


if __name__ == '__main__':
    socket, client_socket = None, None
    try:
        socket = bluetooth.BluetoothSocket(proto=PROTOCOL)
        local_address = 1  # empty local address due to "single adapter" model
        print("Available port:", bluetooth.PORT_ANY)
        socket.bind(("", bluetooth.PORT_ANY))

        uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
        bluetooth.advertise_service(socket, "Desktop controls service", service_id=uuid,
            service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE])

        socket.listen(1)
        # 1. accept a connection
        client_socket, address = socket.accept()
        print("Received connection from", address)

        socket.setblocking(True)
        # 2. listen to commands indefinitely
        while True:
            message = client_socket.recv(128)
            message = message.decode('utf-8').strip()
            if not message:
                continue
            print("Received message:", message)

            key_code = get_code(message)
            if key_code is None:
                continue

            press_release(key_code)

    finally:
        # close sockets after all
        if client_socket is not None:
            client_socket.close()
        if socket is not None:
            bluetooth.stop_advertising(socket)
            socket.close()

    nearby_devices = bluetooth.discover_devices(lookup_names=True)
    print("Found {} devices.".format(len(nearby_devices)))

    for addr, name in nearby_devices:
        print("  {} - {}".format(addr, name))

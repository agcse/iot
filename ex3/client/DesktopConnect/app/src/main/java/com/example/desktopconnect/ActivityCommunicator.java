package com.example.desktopconnect;

import android.bluetooth.BluetoothSocket;
import android.content.Context;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;

public class ActivityCommunicator {
    static public BluetoothSocket socket = null;

    static public AlertDialog createLogDialog(@NonNull Context context, String text) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setMessage(text);
        return builder.create();
    }
}

package com.example.desktopconnect;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ProgressBar;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import java.io.IOException;
import java.util.Set;
import java.util.UUID;
import java.util.Vector;

public class Locate extends AppCompatActivity {
    private UUID uuid = UUID.fromString("1e0ca4ea-299d-4335-93eb-27fcfe7fa848");
    private Vector<BluetoothDevice> devices = new Vector<BluetoothDevice>();
    private BluetoothAdapter adapter = BluetoothAdapter.getDefaultAdapter();
    private final BroadcastReceiver receiver = new BroadcastReceiver() {
        // TODO: discovery stops at some point, see progress bar (unknown reason)
        @Override
        public void onReceive(Context context, Intent intent) {
            ProgressBar progress = findViewById(R.id.locate_progress);
            progress.setProgress((progress.getProgress() + 1) % progress.getMax());
            String action = intent.getAction();
            if (BluetoothAdapter.ACTION_DISCOVERY_STARTED.equals(action)) {
                showDialog("Starting discovery...");
                return;
            }
            if (BluetoothAdapter.ACTION_DISCOVERY_FINISHED.equals(action)) {
                showDialog("Finishing discovery...");
                return;
            }
            if (BluetoothDevice.ACTION_FOUND.equals(action)) {
                BluetoothDevice device = intent.getParcelableExtra(BluetoothDevice.EXTRA_DEVICE);
                if (device == null) {
                    return;
                }
                addDevice(device, context);
            }
        }
    };

    private BluetoothDevice findDevice(String deviceName) {
        for (int i = 0; i < devices.size(); ++i) {
            BluetoothDevice device = devices.elementAt(i);
            if (device.getName().equals(deviceName)) {
                return device;
            }
        }
        return null;
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.locate_activity);

        if (adapter == null) {
            // TODO: handle this case
            showDialog("Adapter is Null");
            return;
        }
        if (!adapter.isEnabled()) {
            Intent enableBluetoothIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
            startActivity(enableBluetoothIntent);
        }
        if (adapter.isDiscovering()) {
            adapter.cancelDiscovery();
        }

        // Make this device discoverable - for pairing/connection
        Intent discoverableIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_DISCOVERABLE);
        discoverableIntent.putExtra(BluetoothAdapter.EXTRA_DISCOVERABLE_DURATION, 300);
        startActivity(discoverableIntent);

        int MY_PERMISSIONS_REQUEST_ACCESS_COARSE_LOCATION = 1;
        ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.ACCESS_COARSE_LOCATION},
                MY_PERMISSIONS_REQUEST_ACCESS_COARSE_LOCATION);
        int MY_PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION = 1;
        ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.ACCESS_FINE_LOCATION},
                MY_PERMISSIONS_REQUEST_ACCESS_FINE_LOCATION);

        // Register for broadcasts when a device is discovered
        IntentFilter filter = new IntentFilter(BluetoothDevice.ACTION_FOUND);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_STARTED);
        filter.addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED);
        registerReceiver(receiver, filter);

        Set<BluetoothDevice> pairedDevices = adapter.getBondedDevices();
        if (pairedDevices.size() > 0) {
            showDialog("Found paired devices...");
            for (BluetoothDevice device : pairedDevices) {
                addDevice(device, this);
            }
        } else {
            adapter.startDiscovery();
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        adapter.cancelDiscovery();

        // Don't forget to unregister the ACTION_FOUND receiver.
        unregisterReceiver(receiver);
    }

    private void startControlActivity(BluetoothSocket socket) {
        try {
            Intent intent = new Intent(this, Control.class);
            ActivityCommunicator.socket = socket;
            startActivity(intent);
        } catch (Exception e) {
            Log.e("LOCATE_START", "Socket's create() method failed", e);
        }
    }

    private void showDialog(String text) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setMessage(text);
        AlertDialog dialog = builder.create();
        dialog.show();
    }

    private void addDevice(BluetoothDevice device, Context context) {
        String deviceName = device.getName();
        if (deviceName == null || deviceName.isEmpty()) {
            return;
        }
        String deviceAddr = device.getAddress();
        if (deviceAddr == null || deviceAddr.isEmpty()) {
            return;
        }

        if (findDevice(deviceName) != null) {
            return;
        }
        devices.add(device);

        Button deviceButton = new Button(context);
        deviceButton.setLayoutParams(
                new LinearLayout.LayoutParams(LinearLayout.LayoutParams.MATCH_PARENT,
                        LinearLayout.LayoutParams.WRAP_CONTENT));
        deviceButton.setText(deviceName);
        deviceButton.setId(View.NO_ID);
        deviceButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Button thisButton = (Button) v;
                BluetoothDevice device = findDevice((String) thisButton.getText());
                // If failed, continue?
                if (device == null) {
                    return;
                }

                ConnectThread thread = new ConnectThread(device);
                thread.start();
            }
        });

        LinearLayout layout = findViewById(R.id.devices_layout);
        layout.addView(deviceButton);
    }

    private class ConnectThread extends Thread {
        public final BluetoothSocket socket;
        private final BluetoothDevice device;
        private final String TAG = "BLUETOOTH_CONNECT_ERROR";

        public ConnectThread(BluetoothDevice device) {
            // Use a temporary object that is later assigned to mmSocket
            // because mmSocket is final.
            BluetoothSocket tmp = null;
            this.device = device;

            try {
                tmp = device.createRfcommSocketToServiceRecord(uuid);
            } catch (IOException e) {
                Log.e(TAG, "Socket's create() method failed", e);
            }
            socket = tmp;
        }

        public void run() {
            // Cancel discovery because it otherwise slows down the connection.
            // TODO: try enabling cancelDiscovery()
//            adapter.cancelDiscovery();

            try {
                // Connect to the remote device through the socket. This call blocks
                // until it succeeds or throws an exception.
                socket.connect();
            } catch (Exception e) {
                // Unable to connect; close the socket and return.
                try {
                    socket.close();
                } catch (IOException closeException) {
                    Log.e(TAG, "Could not close the client socket", closeException);
                }
                return;
            }

            // The connection attempt succeeded. Perform work associated with
            // the connection in a separate thread.
            startControlActivity(socket);
        }

        // Closes the client socket and causes the thread to finish.
        public void cancel() {
            try {
                socket.close();
            } catch (IOException e) {
                Log.e(TAG, "Could not close the client socket", e);
            }
        }
    }
}

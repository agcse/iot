package com.example.desktopconnect;

import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;


public class Control extends AppCompatActivity {
    private BluetoothSocket socket = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.control_activity);

        socket = ActivityCommunicator.socket;
        if (socket == null || !socket.isConnected()) {
            showDialog("Socket is not connected!");
            return;
        }

        // Set up button listeners:
        Button playButton = findViewById(R.id.play_pause_button);
        playButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMessage("PLAY_PAUSE");
            }
        });
        Button nextButton = findViewById(R.id.next_button);
        nextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMessage("NEXT");
            }
        });
        Button prevButton = findViewById(R.id.prev_button);
        prevButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMessage("PREV");
            }
        });
        Button stopButton = findViewById(R.id.stop_button);
        stopButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMessage("STOP");
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        sendMessage("CLOSE_CONNECTION");
        try {
            ActivityCommunicator.socket.close();
            ActivityCommunicator.socket = null;
        } catch (IOException e) {
            showDialog("Failed to close connection");
        }
    }

    private void sendMessage(String message) {
        try {
            OutputStream out = socket.getOutputStream();
            out.write(message.getBytes(StandardCharsets.UTF_8));
            out.flush();
        } catch (Exception e) {
            showDialog("Failed to send message");
        }
    }

    private void showDialog(String text) {
        ActivityCommunicator.createLogDialog(this, text).show();
    }
}

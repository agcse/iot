package com.example.desktopconnect;

import android.bluetooth.BluetoothSocket;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;

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
        Button playButton = (Button)findViewById(R.id.play_pause_button);
        playButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                sendMessage("PLAY_PAUSE");
            }
        });
//        Button nextButton = (Button)findViewById(R.id.next_button);
//        Button prevButton = (Button)findViewById(R.id.prev_button);
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

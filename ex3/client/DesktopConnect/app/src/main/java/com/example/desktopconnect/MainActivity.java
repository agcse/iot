package com.example.desktopconnect;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button locate = (Button)findViewById(R.id.locate_button);
        locate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startLocate(v);
            }
        });
    }

    protected void startLocate(View view) {
        try {
            Intent intent = new Intent(this, Locate.class);
            startActivity(intent);
        }
        catch (Exception e) {
            Log.e("LOCATE_START", "Socket's create() method failed", e);
        }
    }
}

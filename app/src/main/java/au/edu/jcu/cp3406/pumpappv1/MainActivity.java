package au.edu.jcu.cp3406.pumpappv1;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Adapter;
import android.widget.AdapterView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }

    public void menuClicked(View view) {
        Intent intent = new Intent(this, MenuActivity.class);
        final int result = 1;
        startActivityForResult(intent, result);
    }


    public void userProfileClicked(View view) {
    }
}

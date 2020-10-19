package au.edu.jcu.cp3406.pumpappv1;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Adapter;
import android.widget.AdapterView;
import android.widget.Toast;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {
    DBController db;
    TCPController tcp;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        db = new DBController(this);
        tcp = new TCPController(5000,5002);
        Thread thread = new Thread(tcp);
        thread.start();
    }

    public void menuClicked(View view) {
        Intent intent = new Intent(this, MenuActivity.class);
        final int result = 1;
        startActivityForResult(intent, result);
    }

    public void manualButtonClicked(View view) {
        Message.message(this,"PRESS");
//        long id = db.insertBloodEntry(1,1,1);
        ArrayList<ArrayList<Object>> vals = db.getInjectionEntries();
        Log.i("Vals",vals.toString());
        vals = db.getIssueEntries();
        Log.i("Vals",vals.toString());
        vals = db.getBloodEntries();
        Log.i("Vals",vals.toString());
        vals = db.getInfoEntries();
        Log.i("Vals",vals.toString());
        new Thread(new TriggerManualThread()).start();

    }
    class TriggerManualThread implements Runnable{

        @Override
        public void run() {
            tcp.triggerManual();
        }
    }
    public void userProfileClicked(View view) {
    }

    public void bloodHistoryClicked(View view) {
    }

    public void paskInjectionsClicked(View view) {
    }

    public void ResHistoryClicked(View view) {
    }

    public void pastIssuesClicked(View view) {
    }
}

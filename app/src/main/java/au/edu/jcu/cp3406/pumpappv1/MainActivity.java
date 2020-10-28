package au.edu.jcu.cp3406.pumpappv1;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.os.Handler;
import android.text.format.DateUtils;
import android.util.Log;
import android.view.View;
import android.widget.Adapter;
import android.widget.AdapterView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Calendar;

public class MainActivity extends AppCompatActivity {
    DBController db;
    TCPController tcp;
    Handler handler;
    SQLiteDatabase d;
    private TextView bloodTV;
    private TextView insulinLeftTV;
    private TextView insulinTodayTV;
    private TextView batteryTV;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        db = new DBController(this);
        tcp = new TCPController(5000,5002);
        Thread thread = new Thread(tcp);
        thread.start();

        bloodTV=(TextView)findViewById(R.id.bloodSugarView);
        insulinLeftTV=(TextView)findViewById(R.id.InsulinLeftView);
        insulinTodayTV=(TextView)findViewById(R.id.InsulinTodayView);
        batteryTV=(TextView)findViewById(R.id.batteryView);

//        d = db.getReadable();
        handler = new Handler();
        Runnable r = new Runnable() {
            @Override
            public void run() {
                ArrayList<ArrayList<Object>> vals = db.getBloodEntries(2);
                if(vals.size() > 0){
                    bloodTV.setText(vals.get(0).get(3).toString());
                }
                vals = db.getInfoEntries(2);
                if(vals.size() > 0){
                    batteryTV.setText(vals.get(0).get(3).toString());
                    insulinLeftTV.setText(vals.get(0).get(4).toString());
                }
                vals = db.getInjectionEntries();
                if(vals.size() > 0){
                    int sum = 0;
                    Calendar cal = Calendar.getInstance();
                    for (int i = 0;i < vals.size();i++){
                        if(DateUtils.isToday(Long.parseLong(vals.get(i).get(2).toString()))){
                            sum += Long.parseLong(vals.get(i).get(3).toString());
                        }
                    }
                    insulinTodayTV.setText(String.valueOf(sum));
                }
                Log.i("LOOPIN", "LOOP");
                handler.postDelayed(this, 10000); //  delay one second before updating the number
            }
        };
        handler.postDelayed(r, 10000); //  delay one second before updating the number
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
        Log.i("Inject",vals.toString());
        vals = db.getIssueEntries();
        Log.i("Issue",vals.toString());
        vals = db.getBloodEntries();
        Log.i("Blood",vals.toString());
        vals = db.getInfoEntries();
        Log.i("Info",vals.toString());
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

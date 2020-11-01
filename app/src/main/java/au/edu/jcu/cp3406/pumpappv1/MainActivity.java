package au.edu.jcu.cp3406.pumpappv1;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.database.sqlite.SQLiteDatabase;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.text.format.DateUtils;
import android.util.Log;
import android.view.View;
import android.widget.Adapter;
import android.widget.AdapterView;
import android.widget.TextView;
import android.widget.Toast;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.ZoneOffset;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;
import java.util.TimeZone;

public class MainActivity extends AppCompatActivity {
    DBController db;
    TCPController tcp;
    Handler handler;
    SQLiteDatabase d;
    private TextView bloodTV;
    private TextView insulinLeftTV;
    private TextView insulinTodayTV;
    private TextView batteryTV;
    private TextView messagesTV;
    private TextView messageHistory1TV;
    private TextView messageHistory2TV;
    private TextView messageHistory3TV;
    private TextView dateTimeTV;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        db = new DBController(this);
        tcp = new TCPController("10.0.2.2",5002);
        Thread thread = new Thread(tcp);
        thread.start();

        bloodTV=(TextView)findViewById(R.id.bloodSugarView);
        insulinLeftTV=(TextView)findViewById(R.id.InsulinLeftView);
        insulinTodayTV=(TextView)findViewById(R.id.InsulinTodayView);
        batteryTV=(TextView)findViewById(R.id.batteryView);
        messagesTV = (TextView)findViewById(R.id.MainScreenMessages);
        messageHistory1TV = (TextView)findViewById(R.id.MessageHistory1);
        messageHistory2TV = (TextView)findViewById(R.id.MessageHistory2);
        messageHistory3TV = (TextView)findViewById(R.id.MessageHistory3);
        dateTimeTV = (TextView)findViewById(R.id.DateTimeView);


//        d = db.getReadable();
        handler = new Handler();
        Runnable r = new Runnable() {
            @SuppressLint("DefaultLocale")
            @RequiresApi(api = Build.VERSION_CODES.O)
            @Override
            public void run() {
                ArrayList<ArrayList<Object>> vals = db.getBloodEntries(2);
                ArrayList<ArrayList<Object>> issue_vals = db.getIssueEntries(2);
                if(vals.size() > 0){
                    bloodTV.setText(vals.get(0).get(3).toString());
                    Long millis = (Long) vals.get(0).get(2);
                    LocalDateTime localDateTime = LocalDateTime.ofEpochSecond(millis,0,ZoneOffset.UTC);
                    String full_string = String.format("DATE %d-%s-%d TIME %d:%d:%d",localDateTime.getDayOfMonth(), localDateTime.getMonth(), localDateTime.getYear(), localDateTime.getHour(), localDateTime.getMinute(), localDateTime.getSecond());
//                    messagesTV.setText(full_string);
//                    Date date = new Date(millis);
//                    SimpleDateFormat sdf = new SimpleDateFormat("EEEE,MMMM d,yyyy h:mm,a", Locale.ENGLISH);
//                    sdf.setTimeZone(TimeZone.getTimeZone("UTC"));
//                    String formattedDate = sdf.format(date);
//                    LocalDateTime dateTime = LocalDateTime.ofEpochSecond(secs,0, ZoneOffset.UTC);
//                    LocalDateTime currentDateTime = LocalDateTime.now();
//                    String date_time_string = String.format("%d-%s-%d %d:%d:%d", currentDateTime.getDayOfMonth(), currentDateTime.getMonth(), currentDateTime.getYear(), currentDateTime.getHour(), currentDateTime.getMinute(), currentDateTime.getSecond());
                    dateTimeTV.setText(full_string);
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
                vals = db.getIssueEntries();
                if(vals.size() >0){
                    Long millis = (Long) vals.get(0).get(2);
                    String issue = (String) vals.get(0).get(3);
                    LocalDateTime localDateTime = LocalDateTime.ofEpochSecond(millis,0,ZoneOffset.UTC);
                    String full_string = String.format("DATE: %d-%s-%d TIME %d:%d:%d - %s",localDateTime.getDayOfMonth(), localDateTime.getMonth(), localDateTime.getYear(), localDateTime.getHour(), localDateTime.getMinute(), localDateTime.getSecond(),issue);
                    messagesTV.setText(full_string);
                    millis = (Long) vals.get(0).get(2);
                    issue = (String) vals.get(0).get(3);
                    localDateTime = LocalDateTime.ofEpochSecond(millis,0,ZoneOffset.UTC);
                    full_string = String.format("DATE: %d-%s-%d TIME %d:%d:%d - %s",localDateTime.getDayOfMonth(), localDateTime.getMonth(), localDateTime.getYear(), localDateTime.getHour(), localDateTime.getMinute(), localDateTime.getSecond(),issue);
                    messageHistory1TV.setText(full_string);
                    millis = (Long) vals.get(1).get(2);
                    issue = (String) vals.get(2).get(3);
                    localDateTime = LocalDateTime.ofEpochSecond(millis,0,ZoneOffset.UTC);
                    full_string = String.format("DATE: %d-%s-%d TIME %d:%d:%d - %s",localDateTime.getDayOfMonth(), localDateTime.getMonth(), localDateTime.getYear(), localDateTime.getHour(), localDateTime.getMinute(), localDateTime.getSecond(),issue);
                    messageHistory2TV.setText(full_string);
                    millis = (Long) vals.get(2).get(2);
                    issue = (String) vals.get(2).get(3);
                    localDateTime = LocalDateTime.ofEpochSecond(millis,0,ZoneOffset.UTC);
                    full_string = String.format("DATE: %d-%s-%d TIME %d:%d:%d - %s",localDateTime.getDayOfMonth(), localDateTime.getMonth(), localDateTime.getYear(), localDateTime.getHour(), localDateTime.getMinute(), localDateTime.getSecond(),issue);
                    messageHistory3TV.setText(full_string);
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

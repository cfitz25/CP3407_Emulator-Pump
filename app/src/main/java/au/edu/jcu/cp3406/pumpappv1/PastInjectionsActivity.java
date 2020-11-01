package au.edu.jcu.cp3406.pumpappv1;

import android.annotation.SuppressLint;
import android.database.sqlite.SQLiteDatabase;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.widget.TextView;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.ArrayList;

public class PastInjectionsActivity extends AppCompatActivity {

    public static final int MENU_REQUEST = 123;
    DBController db;
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_past_injections);
        TextView messagesTV = (TextView) findViewById(R.id.CurrentMessage);
        db = new DBController(this);
        ArrayList<ArrayList<Object>> vals = db.getInjectionEntries();
        Long millis = (Long) vals.get(0).get(2);
        Long insulin = (Long) vals.get(0).get(3);
        LocalDateTime localDateTime = LocalDateTime.ofEpochSecond(millis,0, ZoneOffset.UTC);
        @SuppressLint("DefaultLocale") String full_string = String.format("DATE: %d-%s-%d\n TIME: %d:%d:%d \n INSULIN INJECTION: %d",localDateTime.getDayOfMonth(), localDateTime.getMonth(), localDateTime.getYear(), localDateTime.getHour(), localDateTime.getMinute(), localDateTime.getSecond(),insulin);
        messagesTV.setText(full_string);
    }
}
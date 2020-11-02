package au.edu.jcu.cp3406.pumpappv1;

import android.annotation.SuppressLint;
import android.database.sqlite.SQLiteDatabase;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.TextView;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class PastInjectionsActivity extends AppCompatActivity {

    public static final int MENU_REQUEST = 123;
    DBController db;
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_past_injections);
        db = new DBController(this);
        ArrayList<ArrayList<Object>> vals = db.getInjectionEntries();
        List<String> entry_list = new ArrayList<>();
        Long secs;
        Long insulin;
        String new_string;
        LocalDateTime localDateTime;
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        String formattedDate;
        if (vals.size() > 1) {
            for (int i = 0; i < vals.size(); i++) {
                secs = (Long) vals.get(i).get(2);
                insulin = (Long) vals.get(i).get(3);
                localDateTime = LocalDateTime.ofEpochSecond(secs, 0, ZoneOffset.UTC);
                formattedDate = localDateTime.format(dateTimeFormatter);
                new_string = String.format("%s - INSULIN: %s mL", formattedDate, insulin);
                entry_list.add(new_string);
            }
            ListView listView = findViewById(R.id.InsulinListView);
            ArrayAdapter arrayAdapter = new ArrayAdapter(this, R.layout.activity_array, R.id.textView, entry_list);
            listView.setAdapter(arrayAdapter);
        }
    }
}
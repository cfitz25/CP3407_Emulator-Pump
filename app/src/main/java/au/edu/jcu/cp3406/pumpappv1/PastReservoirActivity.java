package au.edu.jcu.cp3406.pumpappv1;

import android.annotation.SuppressLint;
import android.os.Build;
import android.os.Bundle;
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

public class PastReservoirActivity extends AppCompatActivity {

    public static final int MENU_REQUEST = 123;
    DBController db;
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_past_reservoir);
        TextView messagesTV = (TextView) findViewById(R.id.CurrentMessage);
        db = new DBController(this);
        ArrayList<ArrayList<Object>> vals = db.getInfoEntries();
        List<String> entry_list = new ArrayList<>();
        Long secs;
        Long reservoir;
        String new_string;
        LocalDateTime localDateTime;
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        String formattedDate;
        if (vals.size()>1) {
            for (int i = 0; i < vals.size(); i++) {
                secs = (Long) vals.get(i).get(2);
                reservoir = (Long) vals.get(i).get(4);
                localDateTime = LocalDateTime.ofEpochSecond(secs, 0, ZoneOffset.UTC);
                formattedDate = localDateTime.format(dateTimeFormatter);
                new_string = String.format("%s - RESERVOIR: %s mL", formattedDate, reservoir);
                entry_list.add(new_string);
            }
            ListView listView = findViewById(R.id.ReservoirListView);
            ArrayAdapter arrayAdapter = new ArrayAdapter(this, R.layout.activity_array, R.id.textView, entry_list);
            listView.setAdapter(arrayAdapter);
        }
    }
}
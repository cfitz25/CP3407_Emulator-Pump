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

public class PastBloodsugarActivity extends AppCompatActivity {

    public static final int MENU_REQUEST = 123;
    DBController db;
    private TextView messagesTV;

    String new_string;


    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_past_bloodsugar);
        messagesTV = (TextView) findViewById(R.id.CurrentMessage);
        db = new DBController(this);
        ArrayList<ArrayList<Object>> vals = db.getBloodEntries();
        List<String> entry_list = new ArrayList<>();
        Long secs;
        Long blood;
        LocalDateTime localDateTime;
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        String formattedDate;
        for (int i =0; i <vals.size(); i++){
            secs = (Long) vals.get(i).get(2);
            blood = (Long) vals.get(i).get(3);
            localDateTime = LocalDateTime.ofEpochSecond(secs,0, ZoneOffset.UTC);
            formattedDate = localDateTime.format(dateTimeFormatter);
            new_string = String.format("%s - BLOOD: %s cc/L",formattedDate,blood);
            entry_list.add(new_string);
        }
        ListView listView = findViewById(R.id.BloodListView);
        ArrayAdapter arrayAdapter = new ArrayAdapter(this,R.layout.activity_array,R.id.textView, entry_list);
        listView.setAdapter(arrayAdapter);








//        handler = new Handler();
//        Runnable r = new Runnable() {
//            @RequiresApi(api = Build.VERSION_CODES.O)
//            @Override
//            public void run() {
//                ArrayList<ArrayList<Object>> vals = db.getBloodEntries(2);
//                Long millis = (Long) vals.get(0).get(2);
//                int blood = (int) vals.get(0).get(3);
//                LocalDateTime localDateTime = LocalDateTime.ofEpochSecond(millis,0, ZoneOffset.UTC);
//                @SuppressLint("DefaultLocale") String full_string = String.format("DATE: %d-%s-%d\n TIME: %d:%d:%d \n BLOOD SUGAR: %d",localDateTime.getDayOfMonth(), localDateTime.getMonth(), localDateTime.getYear(), localDateTime.getHour(), localDateTime.getMinute(), localDateTime.getSecond(),blood);
//                messagesTV.setText(full_string);
//            }
//        };
    }
}

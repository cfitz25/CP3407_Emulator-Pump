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

public class PastIssuesActivity extends AppCompatActivity {

    public static final int MENU_REQUEST = 123;
    DBController db;
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_past_issues);
        TextView messagesTV = (TextView) findViewById(R.id.CurrentMessage);
        db = new DBController(this);
        ArrayList<ArrayList<Object>> vals = db.getIssueEntries();
        List<String> entry_list = new ArrayList<>();
        Long secs;
        String issue;
        String new_string;
        LocalDateTime localDateTime;
        DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");
        String formattedDate;
        for (int i =0; i <vals.size(); i++){
            secs = (Long) vals.get(i).get(2);
            issue= (String) vals.get(i).get(3);
            localDateTime = LocalDateTime.ofEpochSecond(secs,0, ZoneOffset.UTC);
            formattedDate = localDateTime.format(dateTimeFormatter);
            new_string = String.format("%s - ISSUE: %s", formattedDate, issue.replace("1",""));
            entry_list.add(new_string);
        }
        ListView listView = findViewById(R.id.IssueListView);
        ArrayAdapter arrayAdapter = new ArrayAdapter(this,R.layout.activity_array,R.id.textView, entry_list);
        listView.setAdapter(arrayAdapter);
    }
}
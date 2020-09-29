package au.edu.jcu.cp3406.pumpappv1;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;

public class MenuActivity extends AppCompatActivity {
    public static final int MENU_REQUEST = 123;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
    }

    public void userProfileClicked(View view) {
        Intent intentUserProfile = new Intent(this, ProfileActivity.class);
        final int result = 2;
        startActivityForResult(intentUserProfile, result);
    }

    public void bloodHistoryClocked(View view) {
        Intent intentUserProfile = new Intent(this, pastBloodsugarActivity.class);
        final int result = 2;
        startActivityForResult(intentUserProfile, result);
    }
}

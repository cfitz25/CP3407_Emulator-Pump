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
        Intent intentBloodHistory = new Intent(this, PastBloodsugarActivity.class);
        final int result = 2;
        startActivityForResult(intentBloodHistory, result);
    }
    public void paskInjectionsClicked(View view) {
        Intent intentInjections = new Intent(this, PastInjectionsActivity.class);
        final int result = 3;
        startActivityForResult(intentInjections, result);
    }

    public void ResHistoryClicked(View view) {
        Intent intentResHist = new Intent(this, PastReservoirActivity.class);
        final int result = 4;
        startActivityForResult(intentResHist, result);
    }

    public void pastIssuesClicked(View view) {
        Intent intentPastIssues = new Intent(this,PastIssuesActivity.class);
        final int result = 5;
        startActivityForResult(intentPastIssues, result);
    }


}

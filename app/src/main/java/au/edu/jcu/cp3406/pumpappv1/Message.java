package au.edu.jcu.cp3406.pumpappv1;

import android.content.Context;
import android.util.Log;
import android.widget.Toast;

public class Message {
    public static void message(Context context, String message) {
        Log.i("Message",message);
        Toast.makeText(context, message, Toast.LENGTH_LONG).show();
    }
}
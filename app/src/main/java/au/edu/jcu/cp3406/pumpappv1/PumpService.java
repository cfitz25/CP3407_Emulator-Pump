package au.edu.jcu.cp3406.pumpappv1;

import android.app.Application;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import androidx.annotation.Nullable;

public class PumpService extends Service {
    TCPController tcp_controller;
    DBController db_controller;
    public DBController getDBController(){
        return db_controller;
    }
    public TCPController getTCPController(){
        return tcp_controller;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onCreate() {
        super.onCreate();
        db_controller = new DBController(this);
        tcp_controller = new TCPController(2000,db_controller);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}

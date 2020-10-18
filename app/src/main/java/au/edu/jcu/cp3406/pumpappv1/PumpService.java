package au.edu.jcu.cp3406.pumpappv1;

import android.app.Application;

public class BackgroundTaskApplication extends Application {
    TCPController tcp_controller;
    DBController db_controller;
    public DBController getDBController(){
        return db_controller;
    }
    public TCPController getTCPController(){
        return tcp_controller;
    }
}

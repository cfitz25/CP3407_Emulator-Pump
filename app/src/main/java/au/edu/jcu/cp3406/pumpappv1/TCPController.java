package au.edu.jcu.cp3406.pumpappv1;

import android.util.Log;

import androidx.annotation.Nullable;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;

public class TCPController implements Runnable{
    InetAddress pump_address;
    int pump_port;
    private BufferedReader input;
    DBController db;
    ArrayList<String> recv_buffer;
    ServerSocket server_socket;
    Socket client_socket;
    SimpleDateFormat sdf;
    private static TCPController instance;
    public static TCPController getInstance(){
        return instance;
    }
    public static void setInstance(TCPController inst){
        TCPController.instance = inst;
    }
    public TCPController(String pump_address, int pump_port){

        try {
            this.pump_address = InetAddress.getByName(pump_address);
        }catch(Exception e){
            Log.e("TCP Connect",e.toString());
        }
        this.pump_port = pump_port;
        recv_buffer = new ArrayList<>();
        sdf = new SimpleDateFormat("yyy-MM-dd HH:mm:ss");
        TCPController.setInstance(this);
    }
    public boolean triggerManual(){
        try {
//            Socket socket = new Socket(pump_address, pump_port);
            if(client_socket == null){
                Log.e("Manual Trigger","invalid client socket");
                return false;
            }
            PrintWriter output = new PrintWriter(client_socket.getOutputStream());
            output.write("TRIGGER_MANUAL");
            output.flush();
//            output.close();
//            socket.close();
            Log.i("Manual Trigger","triggered");
            return true;
        }catch (Exception e){
            Log.e("Manual Trigger",e.toString());
        }
        return false;
    }
    @Override
    public void run() {
        Socket socket;
        DBController db = DBController.getInstance();
        while(true){
//            wait(100);
            try{
                if(client_socket == null || client_socket.isClosed()){
                    try {
                        client_socket = new Socket(pump_address,pump_port);
//                        client_socket.connect();
                    }catch(IOException e){
//                        e.printStackTrace();
                    }
                }else{

//                    socket = server_socket.accept();
//                    pump_address = socket.getInetAddress();
//                    Log.i("Socket run",pump_address.toString());
//                    Log.i("Socket run",socket.getInetAddress().toString());
                    input = new BufferedReader(new InputStreamReader(client_socket.getInputStream()));
                    boolean disconnect = false;
                    while (!client_socket.isClosed() &&  !disconnect) {
                        String message = input.readLine();
                        if(message != null) {
                            Log.i("Loop", message);
                        }else{
                            Log.i("Loop", "null");
                            input.close();
                            client_socket.close();
                            disconnect = true;
                        }
                        if (message != null && message.length() > 0) {
                            String[] split_msg = message.split(" ");
                            try {
                                Date datetime = sdf.parse(split_msg[1] + " " + split_msg[2]);
//                                Log.i("Datetime", datetime.toString());
                                int device_id = Integer.parseInt(split_msg[3]);
                                if (split_msg[0].equals("INSULIN")) {
                                    int dosage = Integer.parseInt(split_msg[4]);
                                    boolean is_manual = Boolean.parseBoolean(split_msg[3]);
                                    long id = db.insertInjectionEntry(device_id,datetime.getTime()/1000,dosage,is_manual);
                                } else if (split_msg[0].equals("ISSUE")) {
//                                    int dosage = Integer.parseInt(split_msg[4]);
//                                    boolean is_manual = Boolean.parseBoolean(split_msg[3]);
                                    String issue = "";
                                    for (int i = 3;i<split_msg.length;i++) {
                                        String tmp = split_msg[i].replace("{","").replace("}","");
                                        issue += tmp + " ";
                                    }
                                    Log.i("Issue",issue);
                                    long id = db.insertIssueEntry(device_id,datetime.getTime()/1000,issue);
                                } else if (split_msg[0].equals("BLOOD")) {
                                    int blood_sugar = Integer.parseInt(split_msg[4]);
                                    long id = db.insertBloodEntry(device_id,datetime.getTime()/1000,blood_sugar);
                                } else if (split_msg[0].equals("DEVICE_INFO")) {
                                    int battery = Integer.parseInt(split_msg[4]);
                                    int insulin = Integer.parseInt(split_msg[5]);
                                    long id = db.insertInfoEntry(device_id,datetime.getTime()/1000,battery,insulin);
                                } else {
                                    //no clue bruh
                                    Log.e("TCP processor","no clue bruh");

                                }
                            } catch (Exception e) {
                                Log.e("Socket Listen", e.toString());
                            }
                            break;
                        }
                    }
                }
            }catch(Exception e){
//                e.printStackTrace();
            }
        }
    }
}

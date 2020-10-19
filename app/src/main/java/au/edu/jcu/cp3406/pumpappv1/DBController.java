package au.edu.jcu.cp3406.pumpappv1;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

import java.util.ArrayList;

public class DBController {
    Context context;
    myDbHelper myhelper;
    private static DBController instance;
    public static DBController getInstance(){
        return instance;
    }
    private static void setInstance(DBController inst){
        DBController.instance = inst;
    }
    public DBController(Context context){
        this.context = context;
        myhelper = new myDbHelper(context);
        DBController.setInstance(this);

    }
    public boolean connectRemote(String address, String username, String password){
        return false;
    }
    public long insertBloodEntry(long device, long time, int sugar){
        SQLiteDatabase dbb = myhelper.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put(myDbHelper.DEVICE,device);
        contentValues.put(myDbHelper.TIME,time);
        contentValues.put(myDbHelper.BLOOD_SUGAR,sugar);
        long id = dbb.insert(myDbHelper.BLOOD_TABLE_NAME, null , contentValues);
        return id;
    }
    public long insertInjectionEntry(long device, long time, int dosage, boolean is_manual){
        SQLiteDatabase dbb = myhelper.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put(myDbHelper.DEVICE,device);
        contentValues.put(myDbHelper.TIME,time);
        contentValues.put(myDbHelper.DOSAGE,dosage);
        contentValues.put(myDbHelper.IS_MANUAL,is_manual);
        long id = dbb.insert(myDbHelper.INJECTION_TABLE_NAME, null , contentValues);
        return id;
    }
    public long insertInfoEntry(long device, long time, int battery, int insulin_amount){
        SQLiteDatabase dbb = myhelper.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put(myDbHelper.DEVICE,device);
        contentValues.put(myDbHelper.TIME,time);
        contentValues.put(myDbHelper.BATTERY,battery);
        contentValues.put(myDbHelper.INSULIN_AMOUNT,insulin_amount);
        long id = dbb.insert(myDbHelper.INFO_TABLE_NAME, null , contentValues);
        return id;
    }
    public long insertIssueEntry(long device, long time, String issue){
        SQLiteDatabase dbb = myhelper.getWritableDatabase();
        ContentValues contentValues = new ContentValues();
        contentValues.put(myDbHelper.DEVICE,device);
        contentValues.put(myDbHelper.TIME,time);
        contentValues.put(myDbHelper.ISSUE,issue);
        long id = dbb.insert(myDbHelper.ISSUE_TABLE_NAME, null , contentValues);
        return id;
    }
    public ArrayList<ArrayList<Object> >  getBloodEntries(){
        SQLiteDatabase db = myhelper.getWritableDatabase();
        String[] columns = {myDbHelper.BLOOD_ENTRY,myDbHelper.DEVICE,myDbHelper.TIME,myDbHelper.BLOOD_SUGAR};
        Cursor cursor =db.query(myDbHelper.BLOOD_TABLE_NAME,columns,null,null,null,null,null);
        ArrayList<ArrayList<Object> > buffer= new ArrayList<>();
        while (cursor.moveToNext())
        {
            ArrayList<Object>  tmp = new ArrayList<>();
            for (String i:
                 columns) {
                tmp.add(cursor.getLong(cursor.getColumnIndex(i)));
            }
            buffer.add(tmp);
        }
        return buffer;
    }
    public ArrayList<ArrayList<Object> >  getInjectionEntries(){
        SQLiteDatabase db = myhelper.getWritableDatabase();
        String[] columns = {myDbHelper.INJECTION_ENTRY,myDbHelper.DEVICE,myDbHelper.TIME,myDbHelper.DOSAGE,myDbHelper.IS_MANUAL};
        Cursor cursor =db.query(myDbHelper.INJECTION_TABLE_NAME,columns,null,null,null,null,null);
        ArrayList<ArrayList<Object> > buffer= new ArrayList<>();
        while (cursor.moveToNext())
        {
            ArrayList<Object>  tmp = new ArrayList<>();
            for (String i:
                    columns) {
                tmp.add(cursor.getLong(cursor.getColumnIndex(i)));
            }
            buffer.add(tmp);
        }
        return buffer;
    }
    public ArrayList<ArrayList<Object> >  getIssueEntries(){
        SQLiteDatabase db = myhelper.getWritableDatabase();
        String[] columns = {myDbHelper.ISSUE_ENTRY,myDbHelper.DEVICE,myDbHelper.TIME,myDbHelper.ISSUE};
        Cursor cursor =db.query(myDbHelper.ISSUE_TABLE_NAME,columns,null,null,null,null,null);
        ArrayList<ArrayList<Object> > buffer= new ArrayList<>();
        while (cursor.moveToNext())
        {
            ArrayList<Object>  tmp = new ArrayList<>();
            for (String i:
                    columns) {
                tmp.add(cursor.getLong(cursor.getColumnIndex(i)));
            }
            buffer.add(tmp);
        }
        return buffer;
    }
    public ArrayList<ArrayList<Object>>  getInfoEntries(){
        SQLiteDatabase db = myhelper.getWritableDatabase();
        String[] columns = {myDbHelper.INFO_ENTRY,myDbHelper.DEVICE,myDbHelper.TIME,myDbHelper.BATTERY,myDbHelper.INSULIN_AMOUNT};
        Cursor cursor =db.query(myDbHelper.INFO_TABLE_NAME,columns,null,null,null,null,null);
        ArrayList<ArrayList<Object>> buffer= new ArrayList<>();
        while (cursor.moveToNext())
        {
            ArrayList<Object> tmp = new ArrayList<>();
            for (String i:
                    columns) {
                tmp.add(cursor.getLong(cursor.getColumnIndex(i)));
            }
            buffer.add(tmp);
        }
        return buffer;
    }
    static class myDbHelper extends SQLiteOpenHelper
    {
        private static final String DATABASE_NAME = "pumpDB";    // Database Name
        private static final String BLOOD_TABLE_NAME = "blood_table";   // Table Name
        private static final String INFO_TABLE_NAME = "info_table";   // Table Name
        private static final String ISSUE_TABLE_NAME = "issue_table";   // Table Name
        private static final String INJECTION_TABLE_NAME = "injection_table";   // Table Name
        private static final int DATABASE_Version = 1;    // Database Version
        private static final String TIME="time";     // Column I (Primary Key)
        private static final String BLOOD_ENTRY="blood_entry";
        private static final String DEVICE="device";
        private static final String BLOOD_SUGAR="blood_sugar";
        private static final String ISSUE_ENTRY="issue_entry";
        private static final String ISSUE="issue";
        private static final String INFO_ENTRY="info_entry";
        private static final String BATTERY="battery";
        private static final String INSULIN_AMOUNT="insulin_amount";
        private static final String INJECTION_ENTRY="injection_entry";
        private static final String DOSAGE="dosage";
        private static final String IS_MANUAL="is_manual";
        private Context context;

        public myDbHelper(Context context) {
            super(context, DATABASE_NAME, null, DATABASE_Version);
            this.context=context;
        }

        public void onCreate(SQLiteDatabase db) {
            String command = "CREATE TABLE "+BLOOD_TABLE_NAME;
            command += " ("+BLOOD_ENTRY+" INTEGER PRIMARY KEY AUTOINCREMENT, ";
            command += DEVICE+" INTEGER, ";
            command += TIME+" INTEGER, ";
            command += BLOOD_SUGAR+" INTEGER);";
            try {
                db.execSQL(command);
            } catch (Exception e) {
                Message.message(context,""+e);
            }
            command = "CREATE TABLE "+INJECTION_TABLE_NAME;
            command += " ("+INJECTION_ENTRY+" INTEGER PRIMARY KEY AUTOINCREMENT, ";
            command += DEVICE+" INTEGER, ";
            command += TIME+" INTEGER, ";
            command += DOSAGE+" INTEGER, ";
            command += IS_MANUAL+" INTEGER);";
            try {
                db.execSQL(command);
            } catch (Exception e) {
                Message.message(context,""+e);
            }
            command = "CREATE TABLE "+ISSUE_TABLE_NAME;
            command += " ("+ISSUE_ENTRY+" INTEGER PRIMARY KEY AUTOINCREMENT, ";
            command += DEVICE+" INTEGER, ";
            command += TIME+" INTEGER, ";
            command += ISSUE+" VARCHAR(256));";
            try {
                db.execSQL(command);
            } catch (Exception e) {
                Message.message(context,""+e);
            }
            command = "CREATE TABLE "+INFO_TABLE_NAME;
            command += " ("+INFO_ENTRY+" INTEGER PRIMARY KEY AUTOINCREMENT, ";
            command += DEVICE+" INTEGER, ";
            command += TIME+" INTEGER, ";
            command += BATTERY+" INTEGER, ";
            command += INSULIN_AMOUNT+" INTEGER);";
            try {
                db.execSQL(command);
            } catch (Exception e) {
                Message.message(context,""+e);
            }
        }

        @Override
        public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            try {
                //Message.message(context,"OnUpgrade");
                String DROP_TABLE = "DROP TABLE IF EXISTS ";
                db.execSQL(DROP_TABLE+BLOOD_TABLE_NAME);
                db.execSQL(DROP_TABLE+INFO_TABLE_NAME);
                db.execSQL(DROP_TABLE+ISSUE_TABLE_NAME);
                db.execSQL(DROP_TABLE+INJECTION_TABLE_NAME);
                onCreate(db);
            }catch (Exception e) {
                Message.message(context,""+e);
            }
        }

        @Override
        public void onDowngrade(SQLiteDatabase db, int oldVersion, int newVersion) {
            try {
               // Message.message(context,"OnDowngrade");
                String DROP_TABLE = "DROP TABLE IF EXISTS ";
                db.execSQL(DROP_TABLE+BLOOD_TABLE_NAME);
                db.execSQL(DROP_TABLE+INFO_TABLE_NAME);
                db.execSQL(DROP_TABLE+ISSUE_TABLE_NAME);
                db.execSQL(DROP_TABLE+INJECTION_TABLE_NAME);
                onCreate(db);
            }catch (Exception e) {
                Message.message(context,""+e);
            }
        }
    }
}

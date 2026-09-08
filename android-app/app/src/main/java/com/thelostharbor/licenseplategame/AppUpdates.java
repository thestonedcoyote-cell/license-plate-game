package com.thelostharbor.licenseplategame;

import android.app.*;
import android.content.*;
import android.content.pm.*;
import android.net.Uri;
import android.os.Build;
import android.provider.Settings;
import android.widget.Toast;
import org.json.*;
import java.io.*;
import java.net.*;
import java.security.MessageDigest;
import java.util.*;
import java.util.concurrent.*;

/** Explicit, signed APK updates from the project's stable GitHub release. */
final class AppUpdates {
  private static final String RELEASE="https://api.github.com/repos/thestonedcoyote-cell/license-plate-game/releases/latest";
  private static final String PREFIX="https://github.com/thestonedcoyote-cell/license-plate-game/releases/download/";
  private final Activity activity;
  private final SharedPreferences prefs;
  private final DownloadManager downloads;
  private final ExecutorService worker=Executors.newSingleThreadExecutor();
  private boolean checking, processing, waitingPermission, readyPromptShown, closed;
  private final BroadcastReceiver receiver=new BroadcastReceiver(){
    public void onReceive(Context c,Intent i){
      if(i.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID,-2)==prefs.getLong("download",-1)) inspectDownload();
    }
  };
  AppUpdates(Activity activity){
    this.activity=activity;prefs=activity.getSharedPreferences("app-updates",0);
    downloads=(DownloadManager)activity.getSystemService(Context.DOWNLOAD_SERVICE);
    IntentFilter f=new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE);
    if(Build.VERSION.SDK_INT>=33)activity.registerReceiver(receiver,f,Context.RECEIVER_EXPORTED);
    else activity.registerReceiver(receiver,f);
  }
  void resume(){
    if(waitingPermission){waitingPermission=false;if(activity.getPackageManager().canRequestPackageInstalls())inspectDownload();}
    else if(prefs.getLong("download",-1)>=0)inspectDownload();
    else if(System.currentTimeMillis()-prefs.getLong("lastCheck",0)>24*60*60*1000L)check(false);
  }
  void close(){closed=true;activity.unregisterReceiver(receiver);worker.shutdownNow();}
  private void ui(Runnable r){activity.runOnUiThread(()->{if(!closed&&!activity.isFinishing())r.run();});}
  private void tell(String s){Toast.makeText(activity,s,Toast.LENGTH_LONG).show();}
  private long version(PackageInfo p){return Build.VERSION.SDK_INT>=28?p.getLongVersionCode():p.versionCode;}
  private PackageInfo installed() throws Exception{return activity.getPackageManager().getPackageInfo(activity.getPackageName(),PackageManager.GET_SIGNATURES);}
  void check(boolean manual){
    if(checking)return;
    if(prefs.getLong("download",-1)>=0){inspectDownload();if(manual)tell("An update is already downloading or ready to install.");return;}
    checking=true;if(manual)tell("Checking for updates…");
    worker.execute(()->{try{
      JSONObject release=readJson(RELEASE);
      if(release.optBoolean("draft")||release.optBoolean("prerelease"))throw new IOException("Not a stable release");
      JSONArray assets=release.getJSONArray("assets");String manifest=null;
      for(int i=0;i<assets.length();i++){JSONObject a=assets.getJSONObject(i);if("update.json".equals(a.getString("name")))manifest=a.getString("browser_download_url");}
      if(manifest==null){ui(()->{if(manual)tell("No app update has been published yet.");});return;}
      if(!safeUrl(manifest))throw new IOException("Unexpected update source");
      JSONObject m=readJson(manifest);long next=m.getLong("versionCode");String url=m.getString("url"),sha=m.getString("sha256");
      if(!safeUrl(url)||!url.endsWith(".apk")||!sha.matches("[a-fA-F0-9]{64}")||!activity.getPackageName().equals(m.getString("applicationId")))throw new IOException("Invalid update metadata");
      prefs.edit().putLong("lastCheck",System.currentTimeMillis()).apply();
      if(next<=version(installed())){ui(()->{if(manual)tell("You have the latest version.");});return;}
      if(m.getInt("minSdk")>Build.VERSION.SDK_INT){ui(()->{if(manual)tell("The next update requires a newer Android version.");});return;}
      if(!manual&&next==prefs.getLong("dismissed",-1))return;
      String name=m.getString("versionName"),notes=m.optString("notes","Improvements and fixes.");
      ui(()->new AlertDialog.Builder(activity).setTitle("Update available · "+name).setMessage(notes+"\n\nDownload the update now? Your collection stays on this device.")
        .setPositiveButton("Download",(d,w)->download(url,sha,next)).setNegativeButton("Later",(d,w)->prefs.edit().putLong("dismissed",next).apply()).show());
    }catch(Exception e){ui(()->{if(manual)tell("Couldn’t check for updates. Try again when you’re online.");});}
    finally{ui(()->checking=false);}});
  }
  static boolean safeUrl(String url){return url.startsWith(PREFIX)&&!url.contains("?")&&!url.contains("#")&&!url.contains("..");}
  private JSONObject readJson(String url) throws Exception{
    // Redirects remain HTTPS. GitHub serves release assets from its signed CDN URLs.
    for(int hops=0;hops<6;hops++){
      URL u=new URL(url);if(!"https".equals(u.getProtocol()))throw new IOException("HTTPS required");
      HttpURLConnection c=(HttpURLConnection)u.openConnection();c.setInstanceFollowRedirects(false);c.setConnectTimeout(12000);c.setReadTimeout(15000);c.setRequestProperty("User-Agent","LicensePlateGame-Android");
      try{
        int status=c.getResponseCode();if(status>=300&&status<400){url=new URL(u,c.getHeaderField("Location")).toString();continue;}
        if(status!=200)throw new IOException("Update check failed");
        try(InputStream in=c.getInputStream();ByteArrayOutputStream out=new ByteArrayOutputStream()){
          byte[] buf=new byte[8192];int n;while((n=in.read(buf))!=-1){if(out.size()+n>512*1024)throw new IOException("Metadata too large");out.write(buf,0,n);}return new JSONObject(out.toString("UTF-8"));
        }
      }finally{c.disconnect();}
    }throw new IOException("Too many redirects");
  }
  private File apk(){return new File(activity.getExternalFilesDir(null),"updates/update.apk");}
  private void download(String url,String sha,long next){
    try{
      File file=apk();if(file.exists()&&!file.delete())throw new IOException("Cannot replace download");
      DownloadManager.Request r=new DownloadManager.Request(Uri.parse(url)).setTitle("License Plate Game update").setDescription("Download the latest version")
        .setMimeType("application/vnd.android.package-archive").setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED)
        .setDestinationInExternalFilesDir(activity,null,"updates/update.apk");
      long id=downloads.enqueue(r);prefs.edit().putLong("download",id).putString("sha",sha).putLong("version",next).apply();tell("Downloading update. You can keep playing.");
    }catch(Exception e){tell("Couldn’t start the download. Please try again.");}
  }
  private void inspectDownload(){
    long id=prefs.getLong("download",-1);if(id<0||processing||readyPromptShown)return;
    try(android.database.Cursor c=downloads.query(new DownloadManager.Query().setFilterById(id))){
      if(c==null||!c.moveToFirst()){clear();return;}
      int status=c.getInt(c.getColumnIndexOrThrow(DownloadManager.COLUMN_STATUS));
      if(status==DownloadManager.STATUS_FAILED){clear();tell("Update download failed. Check again to retry.");return;}
      if(status!=DownloadManager.STATUS_SUCCESSFUL)return;
    }
    processing=true;
    worker.execute(()->{try{
      File file=apk();MessageDigest hash=MessageDigest.getInstance("SHA-256");
      try(InputStream in=new FileInputStream(file)){byte[] b=new byte[32768];int n;while((n=in.read(b))!=-1)hash.update(b,0,n);}
      StringBuilder hex=new StringBuilder();for(byte b:hash.digest())hex.append(String.format(Locale.US,"%02x",b&255));
      if(!hex.toString().equalsIgnoreCase(prefs.getString("sha","")))throw new IOException("Checksum mismatch");
      PackageManager pm=activity.getPackageManager();PackageInfo candidate=pm.getPackageArchiveInfo(file.getPath(),PackageManager.GET_SIGNATURES),current=installed();
      if(candidate==null||!activity.getPackageName().equals(candidate.packageName)||version(candidate)!=prefs.getLong("version",-1)||candidate.applicationInfo.minSdkVersion>Build.VERSION.SDK_INT)throw new IOException("Wrong package");
      if(version(candidate)<=version(current)){ui(this::clear);return;}
      if(candidate.signatures==null||current.signatures==null||!new HashSet<>(Arrays.asList(candidate.signatures)).equals(new HashSet<>(Arrays.asList(current.signatures))))throw new IOException("Signing key mismatch");
      ui(()->{readyPromptShown=true;new AlertDialog.Builder(activity).setTitle("Update ready").setMessage("Android will ask you to confirm installation. Your saved collection will be retained.")
        .setPositiveButton("Install",(d,w)->install(id)).setNegativeButton("Later",null).setOnDismissListener(d->readyPromptShown=false).show();});
    }catch(Exception e){ui(()->{clear();tell("This update could not be verified. It was not installed. Check again to retry.");});}
    finally{ui(()->processing=false);}});
  }
  private void install(long id){
    try{
      if(!activity.getPackageManager().canRequestPackageInstalls()){
        waitingPermission=true;new AlertDialog.Builder(activity).setTitle("Allow app updates")
          .setMessage("Allow License Plate Game to install its updates on the next Android screen, then return here.")
          .setPositiveButton("Open settings",(d,w)->activity.startActivity(new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,Uri.parse("package:"+activity.getPackageName()))))
          .setNegativeButton("Later",(d,w)->waitingPermission=false).show();return;
      }
      Uri uri=downloads.getUriForDownloadedFile(id);if(uri==null)throw new IOException("Download missing");
      activity.startActivity(new Intent(Intent.ACTION_VIEW).setDataAndType(uri,"application/vnd.android.package-archive").addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION));
    }catch(Exception e){waitingPermission=false;tell("Couldn’t open Android’s installer. Check for updates to try again.");}
  }
  private void clear(){long id=prefs.getLong("download",-1);if(id>=0)downloads.remove(id);prefs.edit().remove("download").remove("sha").remove("version").apply();}
}

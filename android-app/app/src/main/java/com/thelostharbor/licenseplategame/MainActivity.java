package com.thelostharbor.licenseplategame;

import android.Manifest;import android.app.Activity;import android.os.Bundle;import android.content.pm.PackageManager;import android.webkit.*;import android.net.Uri;import java.io.*;import java.util.*;

public class MainActivity extends Activity {
  private static final String HOST="app.local"; private static final int CAMERA_REQ=10, LOCATION_REQ=11; private AppUpdates updates; private WebView web; private PermissionRequest pendingCamera; private GeolocationPermissions.Callback pendingGeo; private String pendingGeoOrigin;
  @Override public void onCreate(Bundle b){super.onCreate(b);updates=new AppUpdates(this);web=new WebView(this);setContentView(web);WebSettings s=web.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setDatabaseEnabled(true);s.setGeolocationEnabled(true);s.setMediaPlaybackRequiresUserGesture(false);s.setAllowFileAccess(false);s.setAllowContentAccess(true);web.setWebViewClient(new LocalClient());web.setWebChromeClient(new Chrome());web.loadUrl("https://"+HOST+"/index.html");}
  private class LocalClient extends WebViewClient {
    @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest req){Uri u=req.getUrl();if(!HOST.equals(u.getHost()))return super.shouldInterceptRequest(view,req);String p=u.getPath();if(p==null||p.equals("/"))p="/index.html";try{InputStream in=getAssets().open("www"+p);return new WebResourceResponse(mime(p),"UTF-8",in);}catch(IOException e){return new WebResourceResponse("text/plain","UTF-8",404,"Not Found",Collections.emptyMap(),new ByteArrayInputStream(new byte[0]));}}
    @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest req){Uri u=req.getUrl();if(HOST.equals(u.getHost())){if(req.isForMainFrame()&&"/updates/check".equals(u.getPath())){updates.check(true);return true;}return false;}startActivity(new android.content.Intent(android.content.Intent.ACTION_VIEW,u));return true;}
  }
  private class Chrome extends WebChromeClient {
    @Override public void onPermissionRequest(PermissionRequest r){runOnUiThread(()->{if(Arrays.asList(r.getResources()).contains(PermissionRequest.RESOURCE_VIDEO_CAPTURE)){if(checkSelfPermission(Manifest.permission.CAMERA)==PackageManager.PERMISSION_GRANTED)r.grant(new String[]{PermissionRequest.RESOURCE_VIDEO_CAPTURE});else{pendingCamera=r;requestPermissions(new String[]{Manifest.permission.CAMERA},CAMERA_REQ);}}else r.deny();});}
    @Override public void onGeolocationPermissionsShowPrompt(String origin,GeolocationPermissions.Callback cb){if(checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION)==PackageManager.PERMISSION_GRANTED||checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION)==PackageManager.PERMISSION_GRANTED)cb.invoke(origin,true,false);else{pendingGeo=cb;pendingGeoOrigin=origin;requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION,Manifest.permission.ACCESS_COARSE_LOCATION},LOCATION_REQ);}}
  }
  @Override public void onRequestPermissionsResult(int req,String[] perms,int[] results){super.onRequestPermissionsResult(req,perms,results);boolean ok=results.length>0&&results[0]==PackageManager.PERMISSION_GRANTED;if(req==CAMERA_REQ&&pendingCamera!=null){if(ok)pendingCamera.grant(new String[]{PermissionRequest.RESOURCE_VIDEO_CAPTURE});else pendingCamera.deny();pendingCamera=null;}if(req==LOCATION_REQ&&pendingGeo!=null){pendingGeo.invoke(pendingGeoOrigin,ok,false);pendingGeo=null;pendingGeoOrigin=null;}}
  private String mime(String p){p=p.toLowerCase(Locale.US);if(p.endsWith(".html"))return"text/html";if(p.endsWith(".js"))return"application/javascript";if(p.endsWith(".css"))return"text/css";if(p.endsWith(".svg"))return"image/svg+xml";if(p.endsWith(".webmanifest"))return"application/manifest+json";if(p.endsWith(".json"))return"application/json";return"text/plain";}
  @Override public void onResume(){super.onResume();if(updates!=null)updates.resume();}
  @Override public void onDestroy(){if(updates!=null)updates.close();super.onDestroy();}
  @Override public void onBackPressed(){if(web.canGoBack())web.goBack();else super.onBackPressed();}
}

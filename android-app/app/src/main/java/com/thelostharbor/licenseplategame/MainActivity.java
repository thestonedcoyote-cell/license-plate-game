package com.thelostharbor.licenseplategame;

import android.Manifest;import android.app.Activity;import android.os.Bundle;import android.content.pm.PackageManager;import android.webkit.*;import android.net.Uri;import java.io.*;import java.util.*;

public class MainActivity extends Activity {
  private static final int FILE_REQ=12;
  private ValueCallback<Uri[]> pendingFiles;
  private static final String HOST="app.local"; private static final int CAMERA_REQ=10, LOCATION_REQ=11; private AppUpdates updates; private WebView web; private PermissionRequest pendingCamera; private GeolocationPermissions.Callback pendingGeo; private String pendingGeoOrigin; private int permissionInFlight;
  @Override public void onCreate(Bundle b){super.onCreate(b);updates=new AppUpdates(this);web=new WebView(this);setContentView(web);WebSettings s=web.getSettings();s.setJavaScriptEnabled(true);s.setDomStorageEnabled(true);s.setDatabaseEnabled(true);s.setGeolocationEnabled(true);s.setMediaPlaybackRequiresUserGesture(false);s.setAllowFileAccess(false);s.setAllowContentAccess(true);web.setWebViewClient(new LocalClient());web.setWebChromeClient(new Chrome());web.loadUrl("https://"+HOST+"/index.html");}
  private class LocalClient extends WebViewClient {
    @Override public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest req){Uri u=req.getUrl();if(!HOST.equals(u.getHost()))return super.shouldInterceptRequest(view,req);String p=u.getPath();if(p==null||p.equals("/"))p="/index.html";try{InputStream in=getAssets().open("www"+p);return new WebResourceResponse(mime(p),"UTF-8",in);}catch(IOException e){return new WebResourceResponse("text/plain","UTF-8",404,"Not Found",Collections.emptyMap(),new ByteArrayInputStream(new byte[0]));}}
    @Override public boolean shouldOverrideUrlLoading(WebView view,WebResourceRequest req){Uri u=req.getUrl();if(HOST.equals(u.getHost())){if(req.isForMainFrame()&&"/updates/check".equals(u.getPath())){updates.check(true);return true;}return false;}startActivity(new android.content.Intent(android.content.Intent.ACTION_VIEW,u));return true;}
  }
  private class Chrome extends WebChromeClient {
    @Override public boolean onShowFileChooser(WebView view,ValueCallback<Uri[]> callback,FileChooserParams params){
      if(view.getUrl()==null||!trustedOrigin(view.getUrl()))return false;
      if(pendingFiles!=null)pendingFiles.onReceiveValue(null);
      pendingFiles=callback;
      android.content.Intent intent=new android.content.Intent(android.content.Intent.ACTION_OPEN_DOCUMENT);
      intent.addCategory(android.content.Intent.CATEGORY_OPENABLE);
      ArrayList<String> types=new ArrayList<>();
      for(String accepted:params.getAcceptTypes())for(String type:accepted.split(",")){
        type=type.trim();if(type.equals(".json"))type="application/json";
        if(type.contains("/")&&!types.contains(type))types.add(type);
      }
      intent.setType(types.size()==1?types.get(0):"*/*");
      if(types.size()>1)intent.putExtra(android.content.Intent.EXTRA_MIME_TYPES,types.toArray(new String[0]));
      intent.putExtra(android.content.Intent.EXTRA_ALLOW_MULTIPLE,params.getMode()==FileChooserParams.MODE_OPEN_MULTIPLE);
      try{startActivityForResult(intent,FILE_REQ);}catch(android.content.ActivityNotFoundException e){pendingFiles=null;callback.onReceiveValue(null);}
      return true;
    }
    @Override public void onPermissionRequest(PermissionRequest r){runOnUiThread(()->{
      if(!trustedOrigin(r.getOrigin().toString())||!Arrays.asList(r.getResources()).contains(PermissionRequest.RESOURCE_VIDEO_CAPTURE)){r.deny();return;}
      if(pendingCamera!=null&&pendingCamera!=r)pendingCamera.deny();pendingCamera=r;pumpPermissions();
    });}
    @Override public void onPermissionRequestCanceled(PermissionRequest r){if(pendingCamera==r)pendingCamera=null;}
    @Override public void onGeolocationPermissionsShowPrompt(String origin,GeolocationPermissions.Callback cb){
      if(!trustedOrigin(origin)){cb.invoke(origin,false,false);return;}
      if(pendingGeo!=null)pendingGeo.invoke(pendingGeoOrigin,false,false);pendingGeo=cb;pendingGeoOrigin=origin;pumpPermissions();
    }
    @Override public void onGeolocationPermissionsHidePrompt(){pendingGeo=null;pendingGeoOrigin=null;}
  }
  @Override protected void onActivityResult(int req,int result,android.content.Intent data){
    super.onActivityResult(req,result,data);
    if(req!=FILE_REQ||pendingFiles==null)return;
    ValueCallback<Uri[]> callback=pendingFiles;pendingFiles=null;
    if(result!=RESULT_OK||data==null){callback.onReceiveValue(null);return;}
    android.content.ClipData clips=data.getClipData();
    if(clips!=null){Uri[] uris=new Uri[clips.getItemCount()];for(int i=0;i<uris.length;i++)uris[i]=clips.getItemAt(i).getUri();callback.onReceiveValue(uris);}
    else callback.onReceiveValue(data.getData()==null?null:new Uri[]{data.getData()});
  }
  private boolean trustedOrigin(String origin){Uri u=Uri.parse(origin);return "https".equals(u.getScheme())&&HOST.equals(u.getHost())&&(u.getPort()==-1||u.getPort()==443);}
  private boolean has(String permission){return checkSelfPermission(permission)==PackageManager.PERMISSION_GRANTED;}
  private void pumpPermissions(){
    if(permissionInFlight!=0)return;
    if(pendingCamera!=null){if(has(Manifest.permission.CAMERA)){PermissionRequest r=pendingCamera;pendingCamera=null;r.grant(new String[]{PermissionRequest.RESOURCE_VIDEO_CAPTURE});}else{permissionInFlight=CAMERA_REQ;requestPermissions(new String[]{Manifest.permission.CAMERA},CAMERA_REQ);return;}}
    if(pendingGeo!=null){if(has(Manifest.permission.ACCESS_FINE_LOCATION)||has(Manifest.permission.ACCESS_COARSE_LOCATION)){pendingGeo.invoke(pendingGeoOrigin,true,false);pendingGeo=null;pendingGeoOrigin=null;}else{permissionInFlight=LOCATION_REQ;requestPermissions(new String[]{Manifest.permission.ACCESS_FINE_LOCATION,Manifest.permission.ACCESS_COARSE_LOCATION},LOCATION_REQ);}}
  }
  @Override public void onRequestPermissionsResult(int req,String[] perms,int[] results){
    super.onRequestPermissionsResult(req,perms,results);
    if(req==CAMERA_REQ&&pendingCamera!=null){PermissionRequest r=pendingCamera;pendingCamera=null;if(has(Manifest.permission.CAMERA))r.grant(new String[]{PermissionRequest.RESOURCE_VIDEO_CAPTURE});else r.deny();}
    if(req==LOCATION_REQ&&pendingGeo!=null){pendingGeo.invoke(pendingGeoOrigin,has(Manifest.permission.ACCESS_FINE_LOCATION)||has(Manifest.permission.ACCESS_COARSE_LOCATION),false);pendingGeo=null;pendingGeoOrigin=null;}
    if(req==permissionInFlight)permissionInFlight=0;pumpPermissions();
  }
  private String mime(String p){p=p.toLowerCase(Locale.US);if(p.endsWith(".html"))return"text/html";if(p.endsWith(".js"))return"application/javascript";if(p.endsWith(".css"))return"text/css";if(p.endsWith(".svg"))return"image/svg+xml";if(p.endsWith(".webmanifest"))return"application/manifest+json";if(p.endsWith(".json"))return"application/json";return"text/plain";}
  @Override public void onResume(){super.onResume();if(updates!=null)updates.resume();}
  @Override public void onDestroy(){if(updates!=null)updates.close();super.onDestroy();}
  @Override public void onBackPressed(){if(web.canGoBack())web.goBack();else super.onBackPressed();}
}

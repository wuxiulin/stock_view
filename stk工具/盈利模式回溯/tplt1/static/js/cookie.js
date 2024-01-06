//½Å±¾²Ù×÷cookie
var expiryHours = 24;

function SetCookie(name, value, hours){		  
  if (String(name) == "undefined" || name == null || name == "" ) return;
  var expire = "";
  if(hours != null)  {
    expire = new Date((new Date()).getTime() + hours * 600000);
    expire = "; expires=" + expire.toGMTString();
  }
  //alert(name + "=" + escape(value) + expire);
  document.cookie = name + "=" + escape(value) + expire;
}


function RemoveCookie(name) {
 SetCookie( name, '', -1 );
}


function ClearCookie() {
 var name, a = document.cookie.split( ";" );
 
 for(var i=0; i<a.length; i++ ) {
  name = a[i].split( "=" );
  if (name.length>0) RemoveCookie(name[0]);
 }
}


function Combine(){
 var args = Combine.arguments;
 var result = "";
 for(var i=0; i<args.length; i++ ){
  if (String(args[i])!= 'undefined' && args[i] != null && args[i]!= "" ) {
   if (result != "" ) result += ",";
   result += args[i];
  }
 }
 return result;
}


function ExistsCookieValue( name, value ) {
 var v = GetCookie( name );
 if (String(v) == "undefined" || v == null || v == "" ) return false;
 var a = v.split( ',' );
 for( var i= 0; i<a.length; i++ ) {
  if ( a[i] == value) return true;
 }
 return false;
}


function ExistsCookieKey( key ) {
 if (String(key) == "undefined" || key == null || key == "" ) return false;
 var name, a = document.cookie.split( ';' );
 for( var i= 0; i<a.length; i++ ) {
  name = a[i].split( "=" );
  if ( name.length>0 && name[0]==key) return true;
 }
 return false;
}


function AppendCookie(name, value, hours) {
 if (ExistsCookieValue(name,value)) return;
 var v = GetCookie( name );
 SetCookie( name, Combine( v, value ), hours );
}


function GetCookie(name){
  var cookieValue = "";
  var search = name + "=";
  if(document.cookie.length > 0) { 
    offset = document.cookie.indexOf(search);
    if (offset != -1)    { 
      offset += search.length;
      end = document.cookie.indexOf(";", offset);
      if (end == -1) end = document.cookie.length;
      cookieValue = unescape(document.cookie.substring(offset, end))
    }
  }
  return cookieValue;
}
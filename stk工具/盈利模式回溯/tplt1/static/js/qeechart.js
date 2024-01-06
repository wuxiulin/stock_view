/**
 * QeeChart鍥捐〃缁勪欢JS閮ㄥ垎
 * @date 2010-10-26
 * @author jinjian2@myhexin.com
 */
(function( window ) {
var QeeChart = function(options){	
		return this.init(options);
	},
	SHOCKWAVE_FLASH = "Shockwave Flash",
	SHOCKWAVE_FLASH_AX = "ShockwaveFlash.ShockwaveFlash",
	FLASH_MIME_TYPE = "application/x-shockwave-flash",
	
	win = window,
	document = window.document,
	nav = navigator,
	ua = navigator.userAgent;

QeeChart.extend = function(property, source) {
	if(typeof property != "string" || property == "") return;
	
	destination = QeeChart[property]||{};
	
	for (var key in source) {
	    destination[key] = source[key];
	}
	
	QeeChart[property] = destination;
}

QeeChart.instances = {};
QeeChart.addInstance = function( obj ) {
	if( QeeChart.instances == undefined ) {
		QeeChart.instances = new Object();
	}
	if( obj.movieName ) {
		QeeChart.instances[ obj.movieName ] = obj;
	}
};
QeeChart.getInstance = function(name) {
	if(!QeeChart.instances) return null;
	var mvName = "QeeChart_"+name;
	return (QeeChart.instances[mvName] == undefined)?null:QeeChart.instances[mvName];
};
//鑾峰彇娴忚鍣ㄧ増鏈� Object = { type: [webkit|opera|msie|mozilla], version: versionString, player: flashPlayerVersion }
QeeChart.browser = (function( ua ) {
	var playerVersion = [0,0,0],
	d = null,
	ua = ua.toLowerCase();

	var match = /(webkit)[ \/]([\w.]+)/.exec( ua ) ||
		/(opera)(?:.*version)?[ \/]([\w.]+)/.exec( ua ) ||
		/(msie) ([\w.]+)/.exec( ua ) ||
		!/compatible/.test( ua ) && /(mozilla)(?:.*? rv:([\w.]+))?/.exec( ua ) ||
	  	[];
	
	if (typeof nav.plugins != undefined && typeof nav.plugins[SHOCKWAVE_FLASH] == "object") {
		d = nav.plugins[SHOCKWAVE_FLASH].description;
		if (d && !(typeof nav.mimeTypes != undefined && nav.mimeTypes[FLASH_MIME_TYPE] && !nav.mimeTypes[FLASH_MIME_TYPE].enabledPlugin)) { 
			d = d.replace(/^.*\s+(\S+\s+\S+$)/, "$1");
			playerVersion[0] = parseInt(d.replace(/^(.*)\..*$/, "$1"), 10);
			playerVersion[1] = parseInt(d.replace(/^.*\.(.*)\s.*$/, "$1"), 10);
			playerVersion[2] = /[a-zA-Z]/.test(d) ? parseInt(d.replace(/^.*[a-zA-Z]+(.*)$/, "$1"), 10) : 0;
		}
	}else if (typeof win.ActiveXObject != undefined) {
		try {
			var a = new ActiveXObject(SHOCKWAVE_FLASH_AX);
			if (a) { // a will return null when ActiveX is disabled
				d = a.GetVariable("$version");
				if (d) {
					d = d.split(" ")[1].split(",");
					playerVersion = [parseInt(d[0], 10), parseInt(d[1], 10), parseInt(d[2], 10)];
				}
			}
		} catch(e) {}
	}
	
	return { type: match[1] || "", version: match[2] || "0", player: playerVersion };
})(ua);

QeeChart.extend("console", {
	log:	function(msg){
		if(this.consoleQueue.length >= 100){
			this.consoleQueue.shift();
		}
		this.consoleQueue.push(msg);
	},
	clear:	function(){
		this.consoleQueue = [];
	},
	display: function(){
		alert(this.consoleQueue.join("\n"));
	},
	consoleQueue: []
});

QeeChart.prototype = {
	init: function( options ) {
		this.setting = options||{};
		var str = this.setting.name||Math.round(Math.random()*(new Date()).getTime());
		if(QeeChart.getInstance(str) != null) str = Math.round(Math.random()*(new Date()).getTime());
		this.movieName = "QeeChart_"+str;
		this.height = this.setting.height||62;
		this.width = this.setting.width||22;
		this.swfUrl = this.setting.swfUrl;
		this.config = this.setting.config;
		this.legendItemClick = this.setting.onLegendClick;
		
		if(this.setting.dataUrl){
			this.dataUrl = this.setting.dataUrl;
			this.methodQueue.push({"fun":"setDataUrl", "arg": [this.setting.dataUrl]});
		}else if(this.setting.data){
			this.data = this.setting.data;
			this.methodQueue.push({"fun":"setData", "arg": [this.setting.data.data, this.setting.data.type]});
		}
		
		return this;
	},
	appendTo: function( id ) {
		var cnt,
		v = this.swfVersion.split("."),
		pv = QeeChart.browser.player,
		strType = typeof( id );
		if( strType.toLowerCase() == "object" ) {
			cnt = id;
		} else if(id.toString()!=""){
		  cnt = document.getElementById(id.toString());
		}
		
		if( cnt == null ) { 
		  throw "the element( id ) is null "; 
		}
		
		QeeChart.addInstance( this );
		cnt.innerHTML = (pv[0] > v[0] || (pv[0] == v[0] && pv[1] > v[1]) || (pv[0] == v[0] && pv[1] == v[1] && pv[2] >= v[2]))?this.getFlashHtml():this.getFlashInstallHtml();
	},
	getMovie: function () {
		return document.getElementById(this.movieName);//this.movieElement;
	},
	getFlashHtml: function( ) {
		return ['<object type="application/x-shockwave-flash" ',
			'id="',this.movieName,'" name="',this.movieName,'" width="',this.width,'" height="',this.height,'"',
			'data="',this.swfUrl,'" >',
				'<param name="movie" value="',this.swfUrl,'" />',
				'<param name="quality" value="high" />',
				'<param name="allowScriptAccess" value="always" />',
				'<param name="wmode" value="transparent" />',
				'<param name="flashvars" value="',this.getFlashvars(),'" />',
			'</object>'].join("");
	},
	getFlashInstallHtml: function(){
	   return ['<p>鎮ㄧ殑Flash Player鐗堟湰杩囦綆锛屽缓璁偍涓嬭浇鏇存柊鐨刦lashPlayer浠ユ敮鎸佹洿澶氱壒鎬�!</p>',
	   	   '<a href="http://www.adobe.com/go/getflashplayer" target="_blank">',
	           '<img src="http://www.adobe.com/images/shared/download_buttons/get_flash_player.gif" alt="Get Adobe Flash Player" />',
	           '</a>',
	           '<p>瀹夎浠ュ悗寤鸿閲嶆柊鎵撳紑娴忚鍣�!</p>'].join("");
	},
	getFlashvars: function( ) {
			var params = [
			   "movieName="+this.movieName,
			   "config="+encodeURI(this.config)
			];
			if(this.setting.flashvars && toString.apply(this.setting.flashvars) == "[object Object]"){
				var obj = this.setting.flashvars;
				for(var key in obj){
					params.push(key+"="+obj[key]);
				}
			}

			return encodeURI(params.join("&"));
	},
	callFlash: function (functionName, argumentArray) {
		argumentArray = argumentArray || [];
		
	  	//濡傛灉flash鏈噯澶囧ソ
	 	 if(!this.ready){
	    		if(!this.methodQueue) this.methodQueue = [];
	   		this.addLaterCall(functionName, argumentArray);
	    		return;
	  	}
	  	
		//QeeChart.console.log(this.movieName+"	"+functionName+"	"+argumentArray);
		var movieElement = this.getMovie();
		var returnValue, returnString;
		if(movieElement){
			try {
				//returnString = movieElement.CallFunction(__flash__request(functionName, argumentArray));
				returnString = movieElement.CallFunction('<invoke name="' + functionName + '" returntype="javascript">' + __flash__argumentsToXML(argumentArray, 0) + '</invoke>');
				returnValue = eval(returnString);
			 } catch (ex) {
				throw "Call to " + functionName + " failed";
			 }
		 }
		return returnValue;
	},
	delegateFun: function( funName, params ) {
		if( funName in this.setting ) {
			var type = typeof this.setting[funName];
			if( type.toLowerCase()  == "function" ) {
				var fun = this.setting[funName];
				fun.apply( window, params );
			}
		}
	},
	addLaterCall: function(funName, params){
	  if(!funName || funName=="") return;
	  this.methodQueue.push({fun:funName, arg:params});
	},
	clearLaterCall: function(){
	  this.methodQueue = [];
	},
	callLaterMethods: function(){
	  if(!this.methodQueue) return;
	  
	  while(this.methodQueue.length){
	    var obj = this.methodQueue.shift();
	    if(!obj.fun) continue;
	    this.callFlash(obj.fun, obj.arg);
	  }
	},
	flashReady: function(b){
	  this.ready = !!b;
	 // QeeChart.console.log(this.movieName+"	  flashReady  methodQueue.length = "+this.methodQueue.length);
	  if(this.dataUrl && this.dataUrl != ""){
	  	this.addLaterCall("setDataUrl",[this.dataUrl]);
	  }else if(this.data && this.data.data && this.data.type){
	  	this.addLaterCall("setData", [this.data.data, this.data.type]);
	  }
	  if(this.ready) this.callLaterMethods();
	  var mv = this.getMovie();
	  mv.jsReady();
	  return this.movieName;
	},
	onLegendClick: function(id,group){					//褰撻紶鏍囩偣鍑诲浘渚嬩腑鏌愮粍浠舵椂瑙﹀彂, id涓篠eries缂栧彿, group涓篠eries鎵€灞炵粍鐨勭浉鍏充俊鎭牸寮忓锛歿id:0, child:[0,1,2,3]}
		if(typeof(this.legendItemClick) == "function"){
			try{
				return this.legendItemClick(id,group);
			}catch(e){
				throw "onLegendClick undefined or param error, usage: onLegendClick(id,group)";
			}
		}
		return true;
	},
	clearData: function(){	//娓呴櫎鍥捐〃鏁版嵁
		this.callFlash("clearData", []);
	},
	setData: function(data, type){ //璁剧疆鍥捐〃鏄剧ず鏁版嵁 data涓烘暟鎹紝 type涓烘暟鎹被鍨嬶紙榛樿涓�"json")
		if(!data) return;
		type = type||"json";
		this.data = {data:data, type:type};
		if(type=="json" && typeof(data)!="object"){
			if(typeof(data)=="string"){
				try{
					 data = eval(data);
				}catch(e){
					//console.log(e.toString());
				}
			}
			throw "setData: the data type is not 'json'";
		}
	  
	  this.callFlash("setData", [data, type]);
	},
	setDataUrl: function(url){     //缃戠粶杞藉叆鏁版嵁杩樻湭鏀寔
	  if(url==""){
	    throw "setDataUrl: url is empty";
	  }
	  this.dataUrl = url;
	  this.callFlash("setDataUrl",[url]);
	},
	selectItemAt: function(index, seriesIndex, groupId){			//閫夋嫨鏌愬厓绱�
		var serIndex = seriesIndex||0;
		var g = groupId||0;
		this.callFlash("selectItemAt",[index, serIndex, g]);
	},
	clearSelection: function(){							//娓呴櫎閫夋嫨
		this.callFlash("clearSelection", []);
	},
	configChart: function(xml){						//閰嶇疆鏂扮殑鍥捐〃
		var config = xml||"";
		this.callFlash("configChart", [config]);
	},
	configXAxis: function(xml){					//閰嶇疆x杞�
		var config = xml||"";
		this.callFlash("configXAxis", [config]);
	},
	configYAxis: function(xml){					//閰嶇疆y杞�
		var config = xml||"";
		this.callFlash("configYAxis", [config]);
	},
	chartTitle: function(xml){						//閰嶇疆鍥捐〃鏍囬
		var config = xml||"";
		this.callFlash("chartTitle", [config]);
	},
	configLegend: function(xml){				//閰嶇疆渚嬪浘
		var config = xml||"";
		this.callFlash("configLegend", [config]);
	},
	addSeries: function(xml, index, groupId){						//娣诲姞搴忓垪
		var config = xml||"";
		var i = index||-1;
		var g = groupId||0;
		this.callFlash("addSeries", [config, i, g]);
	},
	clearSeries: function(){						//娓呴櫎鎵€鏈夊簭鍒� 
		this.callFlash("clearSeries", []);
	},
	removeSeriesGroup: function(index){			//鍒犻櫎涓€涓簭鍒楃粍
		var i = index||0;
		this.callFlash("removeSeriesGroup", [i]);
	},
	setSeriesVisible: function(value, index, groupId){		//璁剧疆涓€涓簭鍒楁槸鍚﹀彲瑙�
		var i = index||0;
		var g = groupId||0;
		this.callFlash("setSeriesVisible", [value, i, g]);
	},
	getSeriesVisible: function(index, groupId){			//鏌ョ湅涓€涓簭鍒楁槸鍚﹀彲瑙�
		var i = index||0;
		var g = groupId||0;
		return this.callFlash("getSeriesVisible", [i,g]);
	},
	removeSeries: function(index, groupId){				//鍒犻櫎绱㈠紩鎸囧畾搴忓垪
		var g = groupId||0;
		this.callFlash("removeSeries", [index,g]);
	},
	showTip: function(bool, index, groupId){			//鏄惁鏄剧ずflash Tip
		var i = index||-1;
		var g = groupId||0;
		this.callFlash("showTip", [bool, i, g]);
	},
	dispose: function(){			//flash娓呯悊
		this.methodQueue = [];
		legendItemClick = null;
		this.callFlash("dispose", []);
	},

	setting: {},
	movieName: "qeechart_flash", 
	legendItemClick: null,
	height: "100%", 
	width: "100%",
	ready: false,
	config: null,
	data: null,
	dataUrl: null,
	swfUrl: "QeeChart.swf",
    methodQueue:[],
    swfVersion: "10.0.0"
};

/** 
 * Cross-browser SWF removal
 * safely and completely remove a SWF in Internet Explorer
 */
function removeSWF(id) {
	var obj = document.getElementById(id);
	if (obj && obj.nodeName == "OBJECT") {
		if(QeeChart.browser.type == "msie"){
			//obj.style.display = "none";
			(function(){
				if (obj.readyState == 4) {
					removeObjectInIE(id);
				}else{
					setTimeout(arguments.callee, 10);
				}
			})();
		} else {
			obj.parentNode.removeChild(obj);
		}
	}
}

function removeObjectInIE(id) {
	var obj = document.getElementById(id);
	if (obj) {
		for (var i in obj) {
			if (typeof obj[i] == "function") {
				obj[i] = null;
			}
		}
		obj.parentNode.removeChild(obj);
	}
}

/**
 * 褰揑E鍏抽棴鎴栧埛鏂版椂flash杩涜娓呴櫎
 */
var cleanup = function() {
	function onunload(e){
	
		for(var mvName in QeeChart.instances){
			var el = QeeChart.getInstance(mvName);
			if(el) {
				el.ready = false;
				try{ el.dispose(); }catch(e){ };
			}
			if(mvName && mvName != "")
				removeSWF(mvName);
			
			QeeChart.instances[mvName] = null;
		}
		
		QeeChart.instances = null;
	}
	
	if (QeeChart.browser.type == "msie") {
		window.attachEvent("onunload", onunload);
	}else{
		window.addEventListener("unload", onunload, false);
	}
}();

window.QeeChart = QeeChart;

})(window);

$(document).ready(function() {
  var sites = ["https://wp.pl","https://trojmiasto.pl","https://zakopane.pl"];
  
  var sendDate = (new Date()).getTime();

  var img = new Image();

  var times = {};
  var min_time = 9999;
  var min_site = "";
  
  var fun = function(site) { 
  
    var img = new Image(); 
	
	var start = new Date().getTime();
	
	var timer = function() { 
	  var dur = new Date().getTime() - start; 
	  if(dur < min_time) {
		min_time = dur;
		min_site = site; 
		console.log(`Min_site is ${site} with ${dur}`);
	  }
	  console.log( `Site: ${site}: ${dur}ms` ); 
	};
	
	img.onload  = timer;
	img.onerror = timer;	
	
	return img.src = site + "/favicon.ico"; 
  }
  
  sites.forEach(fun);  
 
 
  window.setTimeout(() => {window.location.replace(min_site);}, 1500);
});
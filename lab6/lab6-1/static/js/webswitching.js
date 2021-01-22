$(document).ready(function() {
  var sites = ["https://wp.pl","https://tvp.info","https://facebook.com"]    
  var licznik = 0;
  if(sessionStorage.licznik === undefined) {
	  licznik = 0;
	  sessionStorage.licznik = 0;	  
  }
  else {
	licznik = parseInt(sessionStorage.licznik);
	sessionStorage.licznik = (licznik + 1)%3;
  }  
  window.location.replace(sites[licznik]);
});

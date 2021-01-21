$(document).ready(function() {
  var sites = ["https://wp.pl","https://tvp.info"];
  var switch_probability = 0.67;
    
  var wp = 0;
  var tvp = 0;
  
  var dice = Math.random();
  var site = "";
  
  if(typeof sessionStorage.wp === 'undefined') {
	sessionStorage.wp = 0;
  } else {
	wp = parseInt(sessionStorage.wp);
  }
  
  if(typeof sessionStorage.tvp === 'undefined') {
    sessionStorage.tvp = 0;
  } else {
	tvp = parseInt(sessionStorage.tvp);
  }
  
  if(dice > switch_probability) {
    sessionStorage.tvp = tvp + 1;
	tvp = parseInt(sessionStorage.tvp);
	site = sites[1];
  } else {
	sessionStorage.wp = wp + 1;
	wp = parseInt(sessionStorage.wp);
	site = sites[0];
  }
  
  if(tvp+wp != 0) {
	alert(`Wybrano: ${site}\nPrób: ${tvp+wp}, WP: ${((wp/(tvp+wp))*100).toFixed(2)}%, TVP: ${((tvp/(tvp+wp))*100).toFixed(2)}%`);
  }
  else {
    alert(`Wybrano: ${site}\nPrób: ${tvp+wp}, WP: 0%, TVP: 0%`);
  }
  
  window.location.replace(site);  
  
});

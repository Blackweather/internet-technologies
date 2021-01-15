function fibonacci(num){
  var a = 1, b = 0, temp;

  while (num >= 0){
    temp = a;
    a = a + b;
    b = temp;
    num--;
  }

  return b;
}  

$(document).ready(function() {
  $('#save').click(function(e) {
    e.preventDefault();
    localStorage.username = $("#username").val();
    localStorage.password = $("#password").val();
    console.log("Zapisano " + $("#username").val() + ";" + $("#password").val());
  });
  $('#load').click(function(e) {
    e.preventDefault();
    $("#username").val(localStorage.username);
    $("#usernamelabel").text("");
    $("#password").val(localStorage.password);
    $("#passwordlabel").text("");
    console.log("Wczytano " + localStorage.username + ";" + localStorage.password);
  });
  $('#count_fibonacci').click(function(e) {
    e.preventDefault(); 
    var fibonacciText = $('#which_fibonacci').val();
    localStorage.fibonacci = fibonacci(parseInt(fibonacciText));
    $('#loaded_fibonacci').val(localStorage.fibonacci);
  });
  $('#load_fibonacci').click(function(e) {
    e.preventDefault(); 
    $('#loaded_fibonacci').val(localStorage.fibonacci);
  });
});

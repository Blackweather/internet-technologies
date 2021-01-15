function getBase64Image(img) {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;

    var ctx = canvas.getContext("2d");
    ctx.drawImage(img, 0, 0);

    var dataURL = canvas.toDataURL("image/png");

    return dataURL.replace(/^data:image\/(png|jpg);base64,/, "");
}

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
    $("#password").val(localStorage.password);
    console.log("Wczytano " + localStorage.username + ";" + localStorage.password);
  });
  $('#save_picture').click(function(e) {
    e.preventDefault();
    var img = document.getElementById('imidz');
    imgData = getBase64Image(img);
    localStorage.data = imgData;
  });
  $('#load_picture').click(function(e) {
    e.preventDefault(); 
    $('#imgBox').append('<img id="imidz2"/>');
    $('#imidz2').attr("src", `data:image/jpg;base64,${localStorage.data}`);
    $('#imidz2').attr("width", "200");
  });
  $('#count_fibonacci').click(function(e) {
    e.preventDefault(); 
    var fibonacciText = $('#which_fibonacci').val();
    localStorage.fibonacci = fibonacci(parseInt(fibonacciText));
  });
  $('#load_fibonacci').click(function(e) {
    e.preventDefault(); 
    $('#loaded_fibonacci').val(localStorage.fibonacci);
  });
});

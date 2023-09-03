function sendMail(){
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/inquire", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        name: document.getElementById("name").value,
        phone: document.getElementById("phone").value,
        email: document.getElementById("email").value,
        message: document.getElementById("message").value,

    }));
  document.getElementById("phone").value = "";
  document.getElementById("email").value = "";
  document.getElementById("message").value = "";
  swal("Thanks "+document.getElementById("name").value+"!", "Message sent, We will get back to you!", "success");
  document.getElementById("name").value = "";


}

let on = 'margin-top:5px;background-color:mediumseagreen;color:white'
let off = 'margin-top:5px;background-color:black;color:white'

function AutoOff() {

}


function fname(len) {
  var text = "";

  var charset = "abcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < len; i++)
    text += charset.charAt(Math.floor(Math.random() * charset.length));

  return text;
}


function knightapi(data){
    fetch("/knightclientapi", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(res => {
        swal("Logs deleted", 'Please refresh page', "success");
        //console.log("Request complete! response:", res);
    });
}


function knightapi2(data){
    var hb = document.getElementById("hb2")
    if (hb.innerText == 'Hide post'){
      hb.innerText = 'Unhide post';
      data = {"action":"blog_1","where":data}
      fetch("/knightclientapiv2", {
          method: "POST",
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      }).then(res => {

          swal("Updated", 'Blog post updated', "success");
          document.getElementById("ishidden").value = "1"
          //console.log("Request complete! response:", res);
      });
    }else{
      hb.innerText = 'Hide post';
      data = {"action":"blog_0","where":data}
      fetch("/knightclientapiv2", {
          method: "POST",
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      }).then(res => {

          swal("Updated", 'Blog post updated', "success");
          document.getElementById("ishidden").value = "0"

          //console.log("Request complete! response:", res);
      });
    }
}

function deleapi(d,b){
    fetch("/deleapi", {
        o = {"1":{"table":"blog","column":"route","value":b}}

        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(o[d])
    }).then(res => {
        swal("Logs deleted", 'Please refresh page', "success");
        //console.log("Request complete! response:", res);
    });
}

function updateMod(which, OnOrOff) {

    let data = {};

    if (which == "announcement") {
        v = document.getElementById('announcement_content').value
        if (v) { // process here
            data.module = which;
            data.enabled = OnOrOff;
            data.message = v;
        } else {
            return false
        }
    } else if (which == "popup") {
        im = document.getElementById('popup_img').value
        ms = document.getElementById('popup_message').value
        if (im || ms) { // process here
            data.module = which;
            data.enabled = OnOrOff;
            data.image = im;
            data.message = ms;
        } else {
            return false
        }
    } else if (which == "uparrow") {
        cl = document.getElementById('uparrow_content').value
        if (cl) { // process here
            data.module = which;
            data.enabled = OnOrOff;
            data.color = cl;
        } else {
            return false
        }
    } else if (which == "socialshare") {
        fb = document.getElementById('socialshare_facebook').value;
        ig = document.getElementById('socialshare_instagram').value;
        tw = document.getElementById('socialshare_twitter').value;
        gl = document.getElementById('socialshare_google').value;
        if (fb || ig || tw || gl) { // process here
            data.module = which;
            data.enabled = OnOrOff;
            data.fb = fb;
            data.ig = ig;
            data.tw = tw;
            data.gl = gl;
        } else {
            return false
        }
    }else if (which == "videoembed") {
        cls = document.getElementById('videoembed_code').value
        cls_t = document.getElementById('videoembed_thumbnail').value
        if (cls && cls_t) { // process here
            data.module = which;
            data.enabled = OnOrOff;
            data.code = cls;
            data.thumbnail = cls_t;
        } else {
            return false
        }
    }else if (which == "custom") {
        clss = document.getElementById('custom_code').value
        if (clss) { // process here
            data.module = which;
            data.enabled = OnOrOff;
            data.code = clss;
        } else {
            return false
        }
    }else if (which == "extras") {
        extras_whatsapp = document.getElementById('extras_whatsapp').value
        extras_number = document.getElementById('extras_number').value
        extras_email = document.getElementById('extras_email').value
        extras_address = document.getElementById('extras_address').value
        if (extras_whatsapp || extras_number || extras_email || extras_address) { // process here
            data.module = which;
            data.enabled = OnOrOff;
            data.whatsapp = extras_whatsapp;
            data.number = extras_number;
            data.email = extras_email;
            data.address = extras_address;
        } else {
            return false
        }
    }


    fetch("/module_update", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(res => {
      swal("", 'Module Updated', "success");
        //console.log("Request complete! response:", res);
    });
    return true
}

function OnOff(which) {
    var mod = document.getElementById(which + "_btn");
    if (mod.textContent === "On") { // Turn OFF
        if (updateMod(which, 0)) {
            mod.textContent = "Off";
            mod.style = off
        }

    } else { // Turn ON
        if (updateMod(which, 1)) {
            mod.textContent = "On";
            mod.style = on
        }
    }

}

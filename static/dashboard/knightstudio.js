let on = 'margin-top:5px;background-color:mediumseagreen;color:white';
let off = 'margin-top:5px;background-color:black;color:white';
var product_data = {"id":GenID(),"title":"","category":"","variants":null,"product_url":"","seo_description":"","seo_keywords":"","images":[]};
var variant_data = {};
function AutoOff() {

}

function GenID() {
  return Math.floor(Math.random() * Date.now())
}

function fname(len) {
  let text = "";

  var charset = "abcdefghijklmnopqrstuvwxyz0123456789";

  for (var i = 0; i < len; i++)
    text += charset.charAt(Math.floor(Math.random() * charset.length));

  return text;
}


function knightapi(data) {
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


function knightapi2(data) {
  var hb = document.getElementById("hb2")
  if (hb.innerText == 'Hide post') {
    hb.innerText = 'Unhide post';
    data = {
      "action": "blog_1",
      "where": data
    }
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
  } else {
    hb.innerText = 'Hide post';
    data = {
      "action": "blog_0",
      "where": data
    }
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

function confirm_dedit(key, route) {
  var id = "finald"
  var d = document.getElementById(id).style.display;
  if (d == "none") {
    document.getElementById(id).style.display = "inline-block";
  } else {
    document.getElementById(id).style.display = "none";
  }
}


function confirm_d(key, route, id) {
  var d = document.getElementById(id).style.display;
  if (d == "none") {
    document.getElementById(id).style.display = "block";
  } else {
    document.getElementById(id).style.display = "none";
  }
}

function deleapi(d, b, id) {
  var o = {
    "1": {
      "table": "blog",
      "column": "route",
      "value": b
    }
  }
  fetch("/deleapi", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(o[d])
  }).then(res => {
    if (id === "9999") {
      location.href = "/blog-manage/1";
    } else {
      document.getElementById('tr-' + id).remove();
      swal("Blog manager", 'Blog post deleted', "success");
    }


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
  } else if (which == "videoembed") {
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
  } else if (which == "custom") {
    clss = document.getElementById('custom_code').value
    if (clss) { // process here
      data.module = which;
      data.enabled = OnOrOff;
      data.code = clss;
    } else {
      return false
    }
  } else if (which == "extras") {
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

function p_update(v){
    swal("", 'Variant name required', "error");
}
//
// function icheck(id,maxl){
//     let ids = document.getElementById(id).value;
//     if (ids.lenght < maxl){
//         swal("", 'Variant name required', "error");
//         return false;
//     }
//     return true;
// }

function p_variant_add(e){
    var cont_v=document.getElementById('v-title').value;
    document.getElementById("current-var")
    if (cont_v.length === 0){
      swal("", 'Variant title characters not enough', "error");
      return false;
    }
    if (cont_v in localStorage){
      swal("", 'Variant name Exists', "error");
      return false;
    }else{
      localStorage.setItem(cont_v,JSON.stringify({'price':'0.00','image':''}))
    }

    var cont_vid = cont_v.replace(/[^A-Z0-9]+/ig, "-");
    var newRow=document.getElementById('variant-table').insertRow();
    document.getElementById('variant-notice').style.display = "none";
    newRow.innerHTML = "<tbody>\
    <tr>\
    <td id='td-"+cont_v+"'><b><center><p class='btn-primary text-white rounded'>"+cont_v+"</p></center></b></td> <td id='price-"+cont_v+"'>$0.00</td> <td id='img-"+cont_v+"'>No Image</td><td><button id='btnd-"+cont_v+"' onclick='p_del(this)' class='btn btn-xs border'>Remove</button>&nbsp&nbsp<button class='btn btn-xs border' type='button' id='btn-"+cont_v+"' onclick='openvarmodal(this.id)'>Update</button></td>\
    </tr>\
    </tbody><br>";
    document.getElementById('v-title').value = "";
}


function p_updatevariant(){
    let v = document.getElementById("current-variant-input").value;
    let pr = document.getElementById("p-pricemodal").value;
    let ls = JSON.parse(localStorage.getItem(v));
    ls['price'] = pr;
    document.getElementById("price-"+v).textContent = "$"+pr;
    let regex = /^\d*(\.\d{2})?$/;
    let r = regex.test(pr);   //Boolean

    if (r){
      localStorage.setItem(v,JSON.stringify(ls))
    }else{
      swal("", 'Price value not accepted', "error");
    }

  let myModal = new bootstrap.Modal(document.getElementById('varmodal'), {  keyboard: false });
  myModal.hide();
    // image update add
}

function p_set_settings(dom){
  let n = document.getElementById(dom).value;
  if (!n){
      swal("", 'Variant name required', "error");
    }else{
      localStorage.setItem(dom,n)
    }
}

function p_publish(data){
}

function p_del(r) {
  let i = r.parentNode.parentNode.rowIndex;
  let l = document.getElementById("variant-table").rows.length;
  let b = r.id.replace("btnd-","")
  document.getElementById("variant-table").deleteRow(i);
  localStorage.removeItem(b)
  if (localStorage.length === 0){
      document.getElementById('variant-notice').style.display = "block";
  }
}


function openvarmodal(id){
  let cleared = id.replace("btn-","")
  let cvar = localStorage.getItem(cleared);
  document.getElementById("topModalLabel").textContent = "Update Variant for "+cleared;
  document.getElementById("p-pricemodal").value = JSON.parse(cvar)['price']
  document.getElementById("current-variant-input").value = cleared;
  let myModal = new bootstrap.Modal(document.getElementById('varmodal'), {  keyboard: false });
  myModal.show();

  console.log(product_data)
}

console.log(product_data)

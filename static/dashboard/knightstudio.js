let on = 'margin-top:5px;background-color:mediumseagreen;color:white';
let off = 'margin-top:5px;background-color:black;color:white';
var product_data = {
  "id": GenID(),
  "title": "",
  "category": "",
  "variants": {},
  "product_url": "",
  "seo_description": "",
  "seo_keywords": "",
  "images": [],
  "mainimage": "",
  "body": "",
  "price": "",
  "variant_details": {},
  "hidden":"0",
};
var variant_data = [];
var variant_data_dict = {};
var variant_data_history = {};
var images = [];
var run_once = true;
var err = 0;
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


function delpartialim(data) {
  fetch("/api/delpartialim", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  }).then(res => {
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

function deleapip(d, b, id) {
  var o = {
    "1": {
      "table": "products",
      "column": "product_urlsystem",
      "value": b
    }
  }

  fetch("/deleapip", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(o[d])
  }).then(res => {
    if (id === "9999") {
      location.href = "/product-manage/1";
    } else {
      document.getElementById('tr-' + id).remove();
      swal("Product manager", 'Product deleted', "success");
    }


    //console.log("Request complete! response:", res);
  });
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

function p_update(v) {
  swal("", 'Variant name required', "error");
}

function p_variant_add(e) {
  var cont_v = document.getElementById('v-title').value;
  document.getElementById("current-var")
  if (cont_v.length === 0) {
    swal("", 'Variant name characters not enough', "error");
    return false;
  }

  if (variant_data.includes(cont_v + "-ivar")) {
    swal("", 'Variant name Exists', "error");
    return false;
  }

  var cont_vid = cont_v.replace(/[^A-Z0-9]+/ig, "-");
  var newRow = document.getElementById('variant-table').insertRow();
  document.getElementById('variant-notice').style.display = "none";
  var varid = cont_v + "-ivar"
  newRow.innerHTML = "<tbody>\
    <tr>\
    <td id='td-" + cont_v + "'><b><center><p class='text-dark rounded'>" + cont_v + "</p></center></b></td> <td class='col-1'><input type='number' class='form-control' id='" + cont_v + "-price' placeholder='This variant's price' value='1.00' style='width:80px;padding:0'></input></td><td class='col-1'><input type='number' class='form-control' id='" + cont_v + "-stock' placeholder='How much stock you have' value='1000' style='width:80px;padding:0'></td> <td id='img-" + cont_v + "' class='col-4'><form enctype='multipart/form-data'><input type='file' name='" + varid + "' id='" + varid + "'></form></td><td><button type='button' id='btnd-" + cont_v + "' onclick='p_del(this)' class='btn btn-xs border col-xs-1'>X</button>&nbsp&nbsp</td>\
    </tr>\
    </tbody><br>";
  document.getElementById('v-title').value = "";
  const inputElementvar = document.querySelector(`#` + varid);
  p = FilePond.create(inputElementvar, {
    server: './upload-p-variant',
    credits: false,
    labelIdle: "Drop or Browse..",
    fileMetadataObject: {
      p_id: product_data['id'],
      p_variant: cont_v,
    },
    fileRenameFunction: (file) => {
      return fname(19) + `${file.extension}`;
    }


  }); //pondvar ends

  variant_data.push(varid);
  p.on('addfile', (error, file) => {
    // this object contains the file info
    variant_data_history[cont_v + "-ivar"] = file.file.name
    // file.file.filename = "asdasdasd"
  })
}



function p_updatevariant(ids) {
  let pr = document.getElementById(ids + "-price").value;
}

function p_set_settings(dom) {
  let n = document.getElementById(dom).value;
  if (!n) {
    swal("", 'Value required', "error");
    return false;
  } else {

    if (dom === 'p-desc') {
      product_data['seo_description'] = n;
    } else {
      product_data['seo_keywords'] = n;
    }
  }

  console.log(product_data)
}


function p_del(r) {
  let i = r.parentNode.parentNode.rowIndex;
  let l = document.getElementById("variant-table").rows.length;
  let b = r.id.replace("btnd-", "")
  document.getElementById("variant-table").deleteRow(i);

  // server side del >>>
  try {
    const dt = {
      data: {
        "fid": product_data['id'],
        "filev": variant_data_history[b + "-ivar"]
      }
    };
    const request = axios.delete("/upload-p-variant", dt);
  } catch {
    console.log("unable to delete on backend")
  }


  // server side del <<<

  if (variant_data.length - 1 <= 0) {
    document.getElementById('variant-notice').style.display = "block";
  }
  variant_data = variant_data.filter(v => v !== b + "-ivar");

  if (b + "-ivar" in variant_data_dict) {
    delete variant_data_dict[b + "-ivar"];
  }

}

function validatePrice(input) {
  const regex = new RegExp(/^\$?(?:(?:\d+(?:,\d+)?(?:\.\d+)?)|(?:\.\d+))$/);
  return regex.test(input);
}

function grabvariantdata() {
  var vardata = {};
  for (let i = 0; i < variant_data.length; i++) {
    var _p = document.getElementById(variant_data[i].replace("-ivar", "") + "-price").value
    var _s = document.getElementById(variant_data[i].replace("-ivar", "") + "-stock").value

    if (!validatePrice(_p)) {
      swal("", 'Price not accepted, unable to validate', "error");
      return false;
    }
    if (!validatePrice(_s)) {
      swal("", 'Stocks not accepted, unable to validate', "error");
      return false;
    }

    vardata[variant_data[i]] = {
      'price': _p,
      'instock': _s
    };
    product_data['variant_details'] = vardata;
  }
}

function grabinputs() {
  product_data['images'] = images;
  product_data['title'] = document.getElementById("title").value;
  product_data['price'] = document.getElementById("m-price").value;
  product_data['category'] = document.getElementById("categ").value;
  product_data['product_url'] = document.getElementById("p-url").value;
  product_data['seo_description'] = document.getElementById("p-desc").value;
  product_data['seo_keywords'] = document.getElementById("p-keywords").value;
  product_data['body'] = CKEDITOR.instances['ckeditor'].getData();
  // product_data['images'] = categorydocument.getElementById("categ").value;
  // product_data['mainimage'] = categorydocument.getElementById("categ").value;
  if (product_data['title'].length <= 4) {
    swal("", 'Failed validating title, must contain 5 or more characters', "error");
    return false;
  }
  // if (product_data['product_url'].length <= 4 ){
  //     swal("", 'URL must contain 10 or more characters, or leave blank', "error");
  //     return false;
  // }
  if (product_data['body'].length <= 4) {
    swal("", 'Product description must have 5 or more characters', "error");
    return false;
  }
  if (product_data['price'].length <= 0) {
    swal("", 'Price not accepted, unable to validate', "error");
    return false;
  }
  if (!validatePrice(product_data['price'])) {
    swal("", 'Price not accepted, unable to validate', "error");
    return false;

  }
  return grabvariantdata()
}


function build_variants() {
  for (let i = 0; i < variant_data.length; i++) {
    variant_data_dict[variant_data[i]] = document.getElementsByName(variant_data[i])[0].value
  }
  product_data['variants'] = variant_data_dict
  return grabinputs();

}

function p_publish() {
  // document.getElementById("loading").style = 'display:block';
  // document.getElementById("publishb").style = 'display:none';
  build_variants()
  fetch("/product-publish", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(product_data)
  }).then(res => {
    // swal("", 'Module Updated', "success");
    console.log("Request complete! response:", res);
  });

}

function p_updatepost() {

  // document.getElementById("loading").style = 'display:block';
  // document.getElementById("publishb").style = 'display:none';
  if (build_variants() == false){
    swal("", 'Please check for any missing information.', "error");
  }else{

  fetch("/product-update", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(product_data)
  }).then(res => {
    // swal("", 'Module Updated', "success");
     location.href = "/product/1/"+product_data['product_urlsystem']
  });

}}

function p_variant_add_exists(e, loadimage = null) {
  var cont_v = e; //document.getElementById('v-title').value;

  if (cont_v.length === 0) {
    swal("", 'Variant name characters not enough', "error");
    return false;
  }

  if (variant_data.includes(cont_v + "-ivar")) {
    swal("", 'Variant name Exists', "error");
    return false;
  }

  var cont_vid = cont_v.replace(/[^A-Z0-9]+/ig, "-");
  var newRow = document.getElementById('variant-table').insertRow();
  var varid = cont_v + "-ivar"

  document.getElementById('variant-notice').style.display = "none";
  newRow.innerHTML = "<tbody>\
    <tr>\
    <td id='td-" + cont_v + "'><b><center><p class='text-dark rounded'>" + cont_v + "</p></center></b></td> <td class='col-1'><input type='number' class='form-control' id='" + cont_v + "-price' placeholder='This variant's price' value='1.00' style='width:80px;padding:0'></input></td><td class='col-1'><input type='number' class='form-control' id='" + cont_v + "-stock' placeholder='How much stock you have' value='1000' style='width:80px;padding:0'></td> <td id='img-" + cont_v + "' class='col-4'><form enctype='multipart/form-data'><input type='file' name='" + varid + "' id='" + varid + "'></form></td><td><button type='button' id='btnd-" + cont_v + "' onclick='p_del(this)' class='btn btn-xs border col-xs-1'>X</button>&nbsp&nbsp</td>\
    </tr>\
    </tbody><br>";
  document.getElementById('v-title').value = "";
  const inputElementvar = document.querySelector(`#` + varid);
  p = FilePond.create(inputElementvar, {
    server: './upload-p-variant',
    credits: false,
    labelIdle: "Drop or Browse..",
    fileMetadataObject: {
      p_id: product_data['id'],
      p_variant: cont_v,
    },

  });


  variant_data.push(varid);

  const frm = "/media/variant/" + product_data['id'] + "/" + loadimage;
  //
  p.on('addfile', (error, file) => {
    variant_data_history[cont_v + "-ivar"] = file.file.name
  })

  if (loadimage) {
    p.addFile(frm);
  }


}

function p_dele() {
  build_variants()
  console.log("variant_data >>>", variant_data)
  console.log("variant_data_dict >>>", variant_data_dict)
  console.log("variant_data_history", variant_data_history)
  console.log("images", images)
  console.log("mainimage",product_data['mainimage'])

}

function p_showdel(){
  swal({
      title: "Are you sure?",
      text: "Product files and data will be deleted",
      icon: "warning",
      buttons: [
        'Cancel',
        'Delete'
      ],
      dangerMode: true,
    }).then(function(isConfirm) {
      if (isConfirm) {
          fetch("/product-d", {
            method: "POST",
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({"id":product_data['id']})
          }).then(res => {
            // swal("", 'Module Updated', "success");
            if (res['status']){
              location.href = "/product-manage/1"
            };
          });
      }
    })
}

function p_showhid(){
  if (product_data['hidden'] === "0"){
    product_data['hidden'] = "1";
    let x = document.getElementById("btnh").textContent = "Unhide product"
  }else{
    product_data['hidden'] = "0";
    let x = document.getElementById("btnh").textContent = "Hide product"
  }

}


function kstheme(){
  let tmel = document.getElementById("ktheme");
  let tm = tmel.options[tmel.selectedIndex].text;

  if (!tm){
    swal("", 'No theme selected', "error");
    return false;
  }
  fetch("/api/themeset", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({'set':tm})
  }).then(res => {
    swal("", 'Theme has been updated', "success");
  });
}

function ksthemeprev(){
  
}

function addratespartial(name,amount,min,max,data=false){
  if (data){
    shipping[name] = [amount,min,max]
    shipping_names.push(name)
  }else{
    shipping[name.value] = [amount.value,min.value,max.value]
    shipping_names.push(name.value)
  
    name.value = ""
    amount.value = ""
    min.value = ""
    max.value = ""    
  }
}

function delratespartial(e,ef){
  shipping_names.splice(shipping_names.indexOf(ef), 1);
  delete shipping[ef]

  const element = document.getElementById(e);
  element.remove();
}

function shippingrateel(data=false){
  let coldiv = document.getElementById("rates");
  let sname = document.getElementById("sname")
  let samount = document.getElementById("samount")
  let smin = document.getElementById("sminimum")
  let smax = document.getElementById("smaximum")

  var l = `
     <div class="card shadow-none border rounded-0 p-1 m-1" id="${sname.value.trim()}" style="background:#FDDCA1">
      <div class="card-body">
        <center><h6 class="card-title border p-2 m-2 rounded-2" style="background:#FFC300">${sname.value}</h6></center>
        <center><p class="card-text m-2"><b>Shipping time</b> ${smin.value}-${smax.value} Business Days,  <b>Shipping Cost</b> ${samount.value} ${currkey}</p></center>
        <button type="button" class="btn btn-warning btn-xs border" onclick="delratespartial('${sname.value.trim()}','${sname.value}')">Delete</button>
      </div>
    </div>
  `
  if (data){
      var l = `
            <div class="card shadow-none border rounded-0 p-1 m-1" id="${data[3].trim()}" style="background:#FDDCA1">
              <div class="card-body">
                <center><h6 class="card-title border p-2 m-2 rounded-2" style="background:#FFC300">${data[3]}</h6></center>
                <center><p class="card-text m-2"><b>Shipping time</b> ${data[1]}-${data[2]} Business Days,  <b>Shipping Cost</b> ${data[0]} ${currkey}</p></center>
                <button type="button" class="btn btn-warning btn-xs border" onclick="delratespartial('${data[3].trim()}','${data[3]}')">Delete</button>
              </div>
            </div>
          `
      console.log(l)

  }
if (!data){

  if (!sname.value || !samount.value || !smin.value || !smax.value){
      swal("", 'Some information is missing', "error");
      return false;
  }
  if (isNaN(smin.value) || isNaN(smax.value) || isNaN(samount.value)){
      swal("", 'Cannot validate your input', "error");
      return false;
  }
  if (parseInt(smin.value) >= parseInt(smax.value)){
      swal("", 'Minimum option must be less than Maximum', "error");
      return false;
  }
  if (shipping_names.includes(sname.value)){
      swal("", 'Please choose a different name', "error");
      return false;
  }
}
if (data){
    addratespartial(data[3],data[0],data[1],data[2],data=true)
}else{
   addratespartial(sname,samount,smin,smax)
}

console.log("Adding")
coldiv.insertAdjacentHTML( 'afterbegin',l)

}

function showship(e){
  if (e.value === "on"){
      document.getElementById("shippingopt").style.display = "block";
  }else{
      shipping = {}
      shipping_names = []
      divp = document.getElementById("rates");
      divp.innerHTML = "";
      document.getElementById("shippingopt").style.display = "none";
  }
}

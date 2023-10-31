var tmp_obj = {"fulfilled":email_template_fulfilled,"placed":email_template_placed,"abandoned":email_template_abandoned}
var tmp_status = templates;
var current_tmp = "fulfilled";
var tsel = document.getElementById('tempsel');
var status_e = document.getElementById("tempstatus")


tsel.addEventListener('focus', function (e) {
   tmp_obj[current_tmp] = CKEDITOR.instances['ckeditor'].getData();
});

tsel.addEventListener('change', function (e) {
    current_tmp = e.target.value
    CKEDITOR.instances['ckeditor'].setData(tmp_obj[current_tmp]);
    if (tmp_status[current_tmp] == parseInt(1)){
        status_e.textContent = "Enabled"
    }else{
        status_e.textContent = "Disabled"
    }
    
    const sb = document.getElementById("saver")
    sb.textContent = `Save ${cap(current_tmp)} Order Edit`
});

function cap(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function init_ps(){
    if (tmp_status[current_tmp] == parseInt(1)){
        status_e.textContent = "Enabled"
    }else{
        status_e.textContent = "Disabled"
    }
}

function saveedit(){
   tmp_obj[current_tmp] = CKEDITOR.instances['ckeditor'].getData();
}

function templatestatus(e){
    let st = e.textContent;
    if (st === "Enabled"){
        e.textContent = "Disabled"
        tmp_status[current_tmp] = 0;

    }else{
        e.textContent = "Enabled"
        tmp_status[current_tmp] = 1;
    }
}


function prodapi(api,obj,getret=false){
    let r = document.getElementById("temail")
    let l = document.getElementById("testlog")
    l.value = ""
  fetch(api, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(obj)
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.status == parseInt(1)){
        if (getret){
            let l = document.getElementById("testlog")
            l.value = data.message
            return false;
        }
        swal("Updated", data.message, "success");
        
    }else{
        if (getret){
            let l = document.getElementById("testlog")
            l.value = data.message
            return false;
        }
        swal("Update failed", data.message, "error");
    }
});
}

function prodsettings_sm(){
    let els = {}
    let eserver = document.getElementById("eserver")
    let eport = document.getElementById("eport")
    let eemail = document.getElementById("eemail")
    let epass = document.getElementById("epassword")
    let etls = document.getElementById("tlsstat")
    let essl = document.getElementById("sslstat")
    els.server = eserver.value;
    els.port = eport.value;
    els.email = eemail.value;
    els.password = epass.value;
    els.ssl = essl.textContent;
    els.tls = etls.textContent;
    prodapi("/api/prodset-smtp",els)
}

function prodsettings_temp(){
    prodapi("/api/prodset-temp",{"status":tmp_status,"templates":tmp_obj})
}

function prodsettings_rates(){
    let status = document.getElementById("shipping")
    let selcountries = []
    let checkboxes = document.querySelectorAll('input[type=checkbox]:checked')
    for (var i = 0; i < checkboxes.length; i++) {
        selcountries.push(checkboxes[i].value)
    }
    prodapi("/api/prodset-ship",{"countries":selcountries,"shipping":JSON.stringify(shipping),"status":status.value})
}

function prodsettings_str(){
    let sk = document.getElementById("skey").value
    let pk = document.getElementById("pkey").value
    let wk = document.getElementById("wskey").value
    let ck = document.getElementById("ckey").value
    if (sk && pk && wk && ck){
        prodapi("/api/prodset-str",{"sk":sk,"pk":pk,"wsk":wk,"ck":ck})
    }else{
        swal("Stripe API", 'Missing information', "error");
    }
}

function smtpst(e){
    if (e.textContent == "YES"){
        e.textContent = "NO"
    }else{
        e.textContent = "YES"
    }
}

function smtptest(){
    let r = document.getElementById("temail")
    prodapi("/test-mail",{"receiver":r.value},getret=1)
}
init_ps()
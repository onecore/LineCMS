var custom_template_status = false;
var custom_template = "";

function ckdata_get(){
    let bel = document.getElementById("customtemp_stat")
    if (bel.textContent === "Save for this order"){
        let ck = CKEDITOR.instances.ckeditor.getData();
        custom_template_status = true;
        custom_template = ck;
        bel.textContent = "Use default"
    }
    else{
        custom_template_status = false;
        custom_template = "";
        bel.textContent = "Save for this order"
    }
}

function restruct(d){
    location.reload()
}


async function api_psingle(data){
  await fetch("/api/product-fulfill", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then((response) => response.json())
  .then((data) => {
        if (parseInt(data['status']) === 1){
            swal("", 'Order fulfilled', "success");
            setTimeout(restruct, 2000);

        }else{
            swal("", 'Order failed to fulfill', "error");
        }
});
}

function confl(data,message=null) {
    let d = {
        title: " ",
        text: "Send notification and Mark this order as Fulfilled",
        icon: "info",
        dangerMode: false,
        buttons: [
            'Not now',
            'Fulfill this order'
        ],
    }
    if (message){
        d['text'] = message
    }

    swal(d).then(function(isConfirm) {
        loadingbar()
        if (isConfirm) {
            let status = false;
            if (custom_template_status){
                data['template'] = custom_template;
            }else{
                data['template'] = "";
            }
            
            api_psingle(data)
        }
    })
}


function fulfill_auto(orn){
    let tr = document.getElementById('tinfo');
    let ad = document.getElementById('ainfo');
    let trv = tr.value
    let adv = ad.value
    data = {"ordernumber":orn,"tracking":trv,"additional":adv,"template":""}
    if (trv && adv){
        confl(data)
    }else if (!trv){
        confl(data,"Continue without Tracking information? ")
    }else if (!adv){
        confl(data,"Continue without Additional information?")
    }else{
        confl(data,"Continue with missing information?")
    }

}

function mailmod() {
console.log('asd')
  window.location.href = "mailto:example@gmail.com?subject=enquiry&body=" + mantemp;
}

function fulfill_manual(orn){
    let tr = document.getElementById('tinfo');
    let ad = document.getElementById('ainfo');
    let trv = tr.value
    let adv = ad.value
    data = {"ordernumber":orn,"tracking":trv,"additional":adv,"template":"","manual":true}
    mailmodl()

}
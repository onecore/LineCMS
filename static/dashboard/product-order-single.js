var custom_template_status = false;
var custom_template = null;

function ckdata_get(){
    let bel = document.getElementById("customtemp_stat")
    if (bel.textContent === "Save for this order"){
        let ck = CKEDITOR.instances.ckeditor.getData();
        custom_template_status = ck;
        bel.textContent = "Use default"
    }
    else{
        custom_template_status = false;
        bel.textContent = "Save for this order"
    }
}
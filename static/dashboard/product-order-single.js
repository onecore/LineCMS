var custom_template = false;

function ckdata_get(){
    let bel = document.getElementById("customtemp_stat")
    if (bel.textContent === "Save for this order"){
        let ck = CKEDITOR.instances.ckeditor.getData();
        custom_template = ck;
        bel.textContent = "Use default"
    }
    else{
        custom_template = false;
        bel.textContent = "Save for this order"
    }
}
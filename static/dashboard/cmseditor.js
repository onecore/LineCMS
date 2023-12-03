const einfo = document.getElementById("editinfo")
const editor_ = document.getElementById("editor")
const sel1 = document.getElementById("sel1")
const sel2 = document.getElementById("sel2")
const sel3 = document.getElementById("sel3")

function saved(success=true) {
    if (success){
        swal("", 'File saved!', "success");
    }else{
        swal("", 'File saved!', "error");
    }
}

sel1.addEventListener('change', function (e) {
    let val_ = e.target.value;
    alert(val_)
});

saved()
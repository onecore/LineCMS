const einfo = document.getElementById("editinfo")
const editor_ = document.getElementById("editor")
const sel1 = document.getElementById("sel1")
const sel2 = document.getElementById("sel2")
const sel3 = document.getElementById("sel3")
const data = {temps}

function sourceupdate(file,pattern,load=false){
    var d = {};
    if (load){
        d = {"source":"load","file":file,"pattern":pattern}
    }else{
        d = {"source":"save","file":file,"pattern":pattern}
    }

    fetch("/edit", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(d)
    }).then(res => {
        swal("", 'File saved', "success");
    });

}

sel1.addEventListener('change', function (e) {
    let val_ = e.target.value;
    if (val_ === "th"){

    }
});

sel2.addEventListener('change', function (e) {
    let val_ = e.target.value;
});

sel3.addEventListener('change', function (e) {
    let val_ = e.target.value;
});


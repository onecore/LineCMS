const einfo = document.getElementById("editinfo")
const editor_ = document.getElementById("editor")
const sel1 = document.getElementById("sel1")
const sel2 = document.getElementById("sel2")
const sel3 = document.getElementById("sel3")


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
        sel2.innerHTML = "";
        for (let o in temps) {
            var option = document.createElement("option");
            option.text = o;
            option.value = "th";
            sel2.appendChild(option)
        }
    }else if (val_ === "ts"){
        sel2.innerHTML = "";
        for (let o in temps) {
            var option = document.createElement("option");
            option.text = o;
            option.value = "ts";
            sel2.appendChild(option)
        }
    
    }else if (val_ === "sr"){
        sel2.innerHTML = "";
        let option = document.createElement("option");
            option.text = "Sitemap/Robots";
            option.value = "sr";
            sel2.appendChild(option)

    }else if (val_ === "py"){
        sel2.innerHTML = "";
        for (let o in pyfiles) {
            var option = document.createElement("option");
            option.text = pyfiles[o];
            option.value = "th";
            sel2.appendChild(option)
        }

    }else if (val_ === "sf"){
        sel2.innerHTML = "";
        let option = document.createElement("option");
            option.text = "settings";
            option.value = "sf";
            sel2.appendChild(option)
    }
    
    
});

sel2.addEventListener('change', function (e) {
    let val_ = e.target.value;
    alert("asd")
});

sel3.addEventListener('change', function (e) {
    let val_ = e.target.value;
});


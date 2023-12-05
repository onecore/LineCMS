const einfo = document.getElementById("editinfo")
const editor_ = document.getElementById("editor")
const sel1 = document.getElementById("sel1")
const sel2 = document.getElementById("sel2")
const sel3 = document.getElementById("sel3")

var current = "";

function sourceupdate(s1,s2,s3,load=false){
    var d = {};
    if (load){
        d = {"source":"load","s1":s1,"s2":s2,"s3":s3}
        current = s3;
    }else{
        d = {"source":"save","s1":s1,"s2":s2,"s3":s3}
    }

    fetch("/edit", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(d)
    })
    .then((response) => response.json())
    .then((data) => {
        if ("save" in data){
            einfo.textContent = `File loaded: ${data['file']}  Language: ${data['lang']}`
            swal("", 'File has been saved', "success");

        }else if ("src" in data){
            editor.setValue(data['src'])
            editor.session.setMode(`ace/mode/${data['lang']}`);
            einfo.textContent = `File loaded: ${data['file']}  Language: ${data['lang']}`
        }

});

}

function save_file(){
    if (current){
        sourceupdate(s1.value,editor.getValue(),sel3.options[sel3.selectedIndex].text)
    }
}

function loader_init(){

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
    sel2.dispatchEvent(new Event('change'));
    }else if (val_ === "tl"){
        sel2.innerHTML = "";
        for (let o in temps) {
            var option = document.createElement("option");
            option.text = o;
            option.value = "tl";
            sel2.appendChild(option)
        }
    sel2.dispatchEvent(new Event('change'));
    }else if (val_ === "sr"){
        sel2.innerHTML = "";
        let option = document.createElement("option");
            option.text = "Sitemap/Robots";
            option.value = "sr";
            sel2.appendChild(option)
    sel2.dispatchEvent(new Event('change'));

    }else if (val_ === "py"){
        sel3.innerHTML = "";        
        sel2.innerHTML = "";
        var option2 = document.createElement("option");
        option2.text = "enginepublic"
        option2.value = "enginepublic"
        sel2.appendChild(option2)

        for (let o in pyfiles) {
            var option = document.createElement("option");
            option.text = pyfiles[o];
            option.value = pyfiles[o];
            sel3.appendChild(option)
        }
    sel2.dispatchEvent(new Event('change'));
    }else if (val_ === "sf"){
        sel2.innerHTML = "";
        let option = document.createElement("option");
            option.text = "settings";
            option.value = "sf";
            sel2.appendChild(option)
    sel2.dispatchEvent(new Event('change'));

    }
    
    
});

sel2.addEventListener('change', function (e) {
    let val_ = e.target.value;
    var sel2_t = sel2.options[sel2.selectedIndex].text;
    sel1_val = sel1.value;

    switch (sel1_val) {
        case "sf":
            sel3.innerHTML = "";
            let option = document.createElement("option");
            option.text = "settings.py";
            option.value = "sf";
            sel3.appendChild(option)
            sel3.dispatchEvent(new Event('change'));

            break;

        case "sr":
            sel3.innerHTML = "";
            let k = ['Sitemap.xml','Robots.txt']
            for (let o in k){
                let option = document.createElement("option");
                option.text = k[o];
                option.value = k[o];
                sel3.appendChild(option)
            }
            sel3.dispatchEvent(new Event('change'));
            break;

        case "th": // template
            sel3.innerHTML = "";
            let p = template_files[sel2_t]
            for (let o in p){
                let option = document.createElement("option");
                option.text = p[o];
                option.value = p[o];
                sel3.appendChild(option)
            }
            sel3.dispatchEvent(new Event('change'));

            break;

        case "tl": // static
            sel3.innerHTML = "";
            let pl = static_files[sel2_t];
            for (let i in pl){
                let option = document.createElement("option");
                option.text = pl[i];
                option.value = pl[i];
                sel3.appendChild(option)
            }
            sel3.dispatchEvent(new Event('change'));
            break;
        
        case "py":
            sel3.dispatchEvent(new Event('change'));


    }
});

sel3.addEventListener('change', function (e) {
    let val_ = e.target.value;
    let select_1 = sel1.value
    let select_2 = sel2.options[sel2.selectedIndex].text;

    sourceupdate(select_1,select_2,val_,load=true)

});


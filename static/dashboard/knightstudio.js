let on = 'margin-top:5px;background-color:mediumseagreen;color:white'
let off = 'margin-top:5px;background-color:black;color:white'

function AutoOff() {

}

function knightapi(data){
    fetch("/knightclientapi", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(res => {
        //console.log("Request complete! response:", res);
    });
}

function updateMod(which, OnOrOff) {

    let data = {};

    if (which == "announcement") {
        v = document.getElementById('announcement_content').value
        if (v) { // process here
            data.module = which;
            data.status = OnOrOff;
            data.message = v
        } else {
            return false
        }
    } else if (which == "popup") {
        im = document.getElementById('popup_img').value
        ms = document.getElementById('popup_message').value
        if (im || ms) { // process here
            data.module = which;
            data.status = OnOrOff;
            data.image = im;
            data.message = ms;
        } else {
            return false
        }
    } else if (which == "uparrow") {
        cl = document.getElementById('uparrow_content').value
        if (cl) { // process here
            data.module = which;
            data.status = OnOrOff;
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
            data.status = OnOrOff;
            data.fb = fb;
            data.ig = ig;
            data.tw = tw;
            data.gl = gl;
        } else {
            return false
        }
    }else if (which == "videoembed") {
        cls = document.getElementById('videoembed_code').value
        if (cls) { // process here
            data.module = which;
            data.status = OnOrOff;
            data.code = cls;
        } else {
            return false
        }
    }else if (which == "custom") {
        clss = document.getElementById('custom_code').value
        if (clss) { // process here
            data.module = which;
            data.status = OnOrOff;
            data.code = clss;
        } else {
            return false
        }
    }else if (which == "extras") {
        extras_whatsapp = document.getElementById('extras_whatsapp').value
        extras_number = document.getElementById('extras_number').value
        extras_email = document.getElementById('extras_email').value
        extras_address = document.getElementById('extras_address').value
        if (extras_whatsapp || extras_number || extras_email || extras_address) { // process here
            data.module = which;
            data.status = OnOrOff;
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

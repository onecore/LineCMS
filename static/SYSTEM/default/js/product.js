// product.js - KnightStudio Dashboard

const varselect = document.querySelector('select');
    varselect.addEventListener('change', function (e) {
            var vvalue = e.target.value;
            var varbox = document.getElementById('varsel');
            var seloption = varbox.options[varbox.selectedIndex].text;

            let stockp = document.getElementById('stock');
            if (seloption === "Available variants"){
                  stockp.innerText = "";
            }else{
            console.log(seloption)
                  stockp.innerText = `Variant: ${seloption} - Available in stock: ${productinfo[seloption+"-ivar"]['instock']}`;
            }
});

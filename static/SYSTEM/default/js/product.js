// product.js - KnightStudio Dashboard

const varselect = document.querySelector('select');
    varselect.addEventListener('change', function (e) {
            var vvalue = e.target.value;
            var varbox = document.getElementById('varsel');
            var seloption = varbox.options[varbox.selectedIndex].text;

            let stockp = document.getElementById('stock');
            let pricep = document.getElementById('pricep');

            if (seloption === "Available variants"){
                  stockp.innerText = "";
                  pricep.innerText = `Price: \$${mainprice}`;
            }else{
            console.log(seloption)
                  stockp.innerText = `Variant: ${seloption} - Available in stock: ${productinfo[seloption+"-ivar"]['instock']}`;
                  pricep.innerText = `Price: \$${productinfo[seloption+"-ivar"]['price']}`;
            }
});

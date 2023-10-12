// product.js - KnightStudio Dashboard
// prices and other datas has server-side checks

const varselect = document.querySelector('select');
varselect.addEventListener('change', function (e) {
    let vvalue = e.target.value;
    let varbox = document.getElementById('varsel');
    let seloption = varbox.options[varbox.selectedIndex].text;

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
function isLS(pid){
  if (localStorage.getItem(pid) === null){
    return false;
  }
  return true;
}


function init(){
    if (isLS(pid)){
      document.getElementById('cart').textContent = localStorage.length - 1;
    }else{
      document.getElementById('cart').textContent = localStorage.length;
    }
}
init()

function addls(){
      localStorage.setItem(pid,1);
      if (isLS(pid)){
          document.getElementById('cart').textContent = localStorage.length - 1;
      }else{
          document.getElementById('cart').textContent = localStorage.length;
      }
}

function removels(){
    localStorage.setItem(pid,0)
    document.getElementById('cart').textContent = localStorage.length-1;

}

const varatc = document.getElementById('addtocart');
varatc.addEventListener('click', function (e) {
    let vvalue = document.getElementById('addtocart').textContent;
    if (vvalue.includes("AD")){
      varatc.textContent = "REMOVE FROM CART";
      addls()
    }else{
      varatc.textContent = "ADD TO CART";
      removels()
    }


});

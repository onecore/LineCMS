// product.js - KnightStudio Dashboard
// prices and other datas has server-side checks
var cartcount = 0;
var cartcopy = {};
var productid = pid;
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


function isLS(){
  if (pid in localStorage){
    return true
  }
  return false;
}

function refreshLS(){
  // refresh localStorage objects
  cartcopy = {}; // local use
  cartcount = 0; // local use
  for (let i = 0; i < localStorage.length; i++){
      var key = localStorage.key(i);
      if (localStorage.getItem(key) > 0 && key != "likes"){
        cartcount = cartcount + 1
      };
   }
  cartcopy = {...localStorage}
}

function likesele(addrem){
  if (addrem){
    // add
  }else{
    //remove
  }
}
function likes(e){
        console.log(productid);

    if ("likes" in localStorage){ // already in LS
      var lls = localStorage.getItem("likes");
      if (lls[pid] === 1){
          lls[pid] = 0;
          likesele(0);
          localStorage.setItem('likes',lls)
      }else{
        lls[pid] = 1;
        likesele(1);
          localStorage.setItem('likes',lls)

      }
    }else{
      likesele(1);
      let ini = {}
      ini[productid] = 1
      localStorage.setItem("likes",JSON.stringify(ini))

    }
    console.log(localStorage['likes'])
}

function initLikes(){
  // initialize likes objs

}


function init(){
    // initialize button and localStorage
    initLikes();
    refreshLS();
    var varatci = document.getElementById('addtocart');
    if (isLS()){
          let getobj = localStorage.getItem(pid);
          if (parseInt(getobj) === 1){
              varatci.textContent = "REMOVE FROM CART";
          }else{
              varatci.textContent = "ADD TO CART";
            }
    }else{
        varatci.textContent = "ADD TO CART";
    }
    document.getElementById('cart').value = cartcount;
}

function addls(){
      // 1 for added
      localStorage.setItem(pid,1);
      refreshLS()
      if (isLS()){
          document.getElementById('cart').value = cartcount;
      }else{
          document.getElementById('cart').value = cartcount;
      }
}

function removels(){
    // 0 for not added
    localStorage.setItem(pid,0)
    document.getElementById('cart').value = localStorage.length-1;

}

const varatc = document.getElementById('addtocart');
const ladd = document.getElementById('addtolike');

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


ladd.addEventListener('click', function (e) {
    likes(e);
});

init()

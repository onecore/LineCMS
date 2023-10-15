// product.js - KnightStudio Dashboard
// prices and other datas has server-side sec. checks (modifed data will be refused by the server)
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
          stockp.innerText = `Variant: ${seloption} - Available in stock: ${productinfo[seloption+"-ivar"]['instock']}`;
          pricep.innerText = `Price: \$${productinfo[seloption+"-ivar"]['price']}`;
    }
    variantim(seloption)
});

function variantim(option){
    
}

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
  let atlele = document.getElementById("addtolike");
  if (addrem){
      atlele.style.background = "red";
      atlele.style.color = "white";
  }else{
      atlele.style.background = "white";
      atlele.style.color = "black";
  }
}

function likes(e){
    if ("likes" in localStorage){ // already in LS
      var lls = localStorage.getItem("likes");
      var lls = JSON.parse(lls)
      if (lls[pid] === 1){
          lls[pid] = 0;
          likesele(0);
          localStorage.setItem('likes',JSON.stringify(lls))
      }else{
        lls[pid] = 1;
        likesele(1);
          localStorage.setItem('likes',JSON.stringify(lls))
      }
    }else{
      likesele(1);
      let ini = {}
      ini[productid] = 1
      localStorage.setItem("likes",JSON.stringify(ini))

    }
    reloadLikes()
}

function reloadLikes(){
  let likesc = 0;
  if ("likes" in localStorage){
      var likesobj = JSON.parse(localStorage.getItem("likes"));
      var likesobjkey = Object.keys(likesobj)
      var likesobjlen = Object.keys(likesobj).length
      for (x = 0; x < likesobjlen; x++){
          var v = likesobj[likesobjkey[x]]
          if (v === 1){
            likesc = likesc + 1
          }
      }
  }
  document.getElementById("likescount").textContent = likesc;
}

function initLikes(){
  // initialize likes objs

  let likesobj = JSON.parse(localStorage.getItem("likes"));
  if (pid in likesobj){
      let likecont = likesobj[pid];
      if (parseInt(likecont)){
          likesele(1);
      }else{
          likesele(0);
      }
  }
  reloadLikes();
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

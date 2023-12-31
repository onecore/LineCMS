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
    let pricef = document.getElementById('fprice');

    if (seloption === "Available variants"){
          stockp.innerText = "";
          pricep.innerText = `Price: \$${mainprice}`;
          pricef.value = mainprice;
    }else{
          stockp.innerText = `Variant: ${seloption} - Available in stock: ${productinfo[seloption+"-ivar"]['instock']}`;
          pricep.innerText = `Price: \$${productinfo[seloption+"-ivar"]['price']}`;
          pricef.value = productinfo[seloption+"-ivar"]['price']
    }
    variantim(seloption)
});

function variantim(option){
  // main function makes variant to slide to it's photo
  let x = variants[option+"-ivar"];
  let cur = (vardict[x])
  console.log(x)
  if (x){
    lslide.goToSlide(cur+1);
  }
}

function isLS(){
  if (pid in localStorage){
    return true
  }
  return false;
}

function refreshLS(get=false,checko=false){
  // refresh localStorage objects
  cartcount = 0; // local use
  cartcheck = {}


  for (let i = 0; i < localStorage.length; i++){
      var key = localStorage.key(i);
      if (localStorage.getItem(key)[0] > 0 && key != "likes" && key != "likesall"){
        cartcount = cartcount + 1
        cartcheck[key] = localStorage.getItem(key)
      };
   }


  if (get){
    return cartcount; //length
  }
  if (checko){
    return cartcheck //checkoutobj
  }
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
    if ("likes" in localStorage && "likesall" in localStorage){ // already in LS
      var lls = localStorage.getItem("likes");
      var lls = JSON.parse(lls)

      var llsall = localStorage.getItem("likesall");
      var llsall = JSON.parse(llsall)

      if (lls[pid] === 1){ //remove
          lls[pid] = 0;
          llsall[pid] = []
          likesele(0);
          localStorage.setItem('likes',JSON.stringify(lls))
          localStorage.setItem('likesall',JSON.stringify(llsall))

      }else{              //add
        lls[pid] = 1;
        llsall[pid] = [product_url,product_title]
        likesele(1);
        localStorage.setItem('likes',JSON.stringify(lls))
        localStorage.setItem('likesall',JSON.stringify(llsall))
      }
    }else{
      likesele(1);
      let ini = {}
      let iniall = {}
      ini[productid] = 1
      iniall[productid] = [product_url,product_title]
      localStorage.setItem("likes",JSON.stringify(ini))
      localStorage.setItem("likesall",JSON.stringify(iniall))

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
  let likesobj = null;
  if ("likes" in localStorage){
      likesobj = JSON.parse(localStorage.getItem("likes"));
  }
  if (likesobj){
      if (pid in likesobj){
          let likecont = likesobj[pid];
          if (parseInt(likecont)){
              likesele(1);
          }else{
              likesele(0);
          }
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
      let _quant = document.getElementById('quant').value;
      let _price = document.getElementById('fprice').value;
      let _vari = document.getElementById('varsel');
      let _varis = _vari.options[_vari.selectedIndex].text;
      localStorage.setItem(pid,[1,_price,_quant,_varis]);
      refreshLS()
      if (isLS()){
          document.getElementById('cart').value = cartcount;
      }else{
          document.getElementById('cart').value = cartcount;
      }
}

function removels(){
    // 0 for not added
    localStorage.removeItem(pid)
      refreshLS()
      if (isLS()){
          document.getElementById('cart').value = cartcount;
      }else{
          document.getElementById('cart').value = cartcount;
      }
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


function prepele(){
    let el = document.getElementById("likedrow");

    if ("likes" in localStorage && "likesall" in localStorage){
        let likesobj = JSON.parse(localStorage.getItem("likes"));
        let likesobjkey = Object.keys(likesobj)
        let likesobjlen = Object.keys(likesobj).length
        let infolikes = JSON.parse(localStorage.getItem("likesall"))
        el.innerHTML = "";
        let shouldstop = 0;
        for (i=0; i < likesobjlen; i++){
            let d = likesobjkey[i];
            if (likesobj[d] === 1){
                shouldstop++
                el.innerHTML += `<div class='row'><div class='col-sm'><p class='text-truncate pt-2'>${infolikes[d][1]}</p></div><div class='col-sm'><a type='button' class='btn btn-primary rounded border float-right' href='/product/${infolikes[d][0]}'>View product</a></div></div><hr>`;
            }
        }
        if (!shouldstop){
          return false;
        }
        return true;
    }else{
      return false;
    }
    return false;
}

function checkout(){
  let data = refreshLS(get=0,checko=1)
  let testv = document.getElementById('cart').value
  if (testv==="0"){
    return false;
  }
  console.log(data)

  fetch("/product-checkout", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then((response) => response.json())
  .then((data) => {
    location.href = data.c
});
}

function openlikes(e=null){
  if (prepele()){
      $("#likeModal").modal('show')
  }
}


init()

var cur_page = 1;

async function api_plist(data){
  await fetch("/product-orders", {
    method: "POST",
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then((response) => response.json())
  .then((data) => {
      console.log(data)
        // if (parseInt(data['status']) === 1){
        //     swal("", 'Order fulfilled', "success");
        //     setTimeout(restruct, 2000);

        // }else{
        //     swal("", 'Order failed to fulfill', "error");
        // }
});
}


const lselect = document.getElementById('category')

lselect.addEventListener('change', function (e) {
    const ssearch = document.getElementById("q").value
    let scategory = e.target.value;
    // api_plist(par_)
    let q = `product-list?category=${scategory}&search=${ssearch}&page=1`
    location.href = q
});


function trigg(){
  var event = new Event('change');
  let element = document.getElementById("category")
  element.dispatchEvent(event);
}
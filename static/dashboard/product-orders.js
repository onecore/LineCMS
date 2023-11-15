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


const setperpage = document.getElementById('ostatus')

setperpage.addEventListener('change', function (e) {
    const ppage_ = document.getElementById("perpage")
    const ssearch = document.getElementById("searchb")
    let status_val = e.target.value;
    let searchc = ssearch.value;
    // api_plist(par_)
    let q = `product-orders?status=${status_val}&search=${searchc}&page=${ppge}`
    location.href = q


});

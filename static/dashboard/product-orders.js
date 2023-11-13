async function api_plist(data){
  await fetch("/api/product-ordersp", {
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
    let status_val = e.target.value;
    // let pp_seloption = ppage_val.options[ppage_val.selectedIndex].text;
    console.log(ppage_val)
    const ppage_ = document.getElementById("perpage")
    const ssearch = document.getElementById("searchb")
    let ppagec = ppage_.value;
    let searchc = ssearch.value;
    let par_ = {"p":ppagec,"s":status_val,"q":searchc}
    api_plist(par_)


});

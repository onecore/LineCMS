const lselect = document.getElementById('categorysel')

lselect.addEventListener('change', function (e) {
    const ssearch = document.getElementById("q").value
    let scategory = e.target.value;
    let q = `product-list?category=${scategory}&search=${ssearch}&page=1`
    location.href = q
});


function trigg(){
  var event = new Event('change');
  let element = document.getElementById("categorysel")
  element.dispatchEvent(event);
}
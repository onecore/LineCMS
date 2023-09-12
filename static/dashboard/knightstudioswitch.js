
document.getElementById('announcement_btn').addEventListener('change', (e) => {
  this.checkboxValue = e.target.checked ? 'On' : 'Off';
  if (this.checkboxValue === "On") {
      return updateMod('announcement', 1) ;
  } else {
      return updateMod('announcement', 0)
  }
})


document.getElementById('popup_btn').addEventListener('change', (e) => {
  this.checkboxValue = e.target.checked ? 'On' : 'Off';
  if (this.checkboxValue === "On") {
      return updateMod('popup', 1) ;
  } else {
      return updateMod('popup', 0)
  }
})


document.getElementById('uparrow_btn').addEventListener('change', (e) => {
  this.checkboxValue = e.target.checked ? 'On' : 'Off';
  if (this.checkboxValue === "On") {
      return updateMod('uparrow', 1) ;
  } else {
      return updateMod('uparrow', 0)
  }
})


document.getElementById('socialshare_btn').addEventListener('change', (e) => {
  this.checkboxValue = e.target.checked ? 'On' : 'Off';
  if (this.checkboxValue === "On") {
      return updateMod('socialshare', 1) ;
  } else {
      return updateMod('socialshare', 0)
  }
})


document.getElementById('videoembed_btn').addEventListener('change', (e) => {
  this.checkboxValue = e.target.checked ? 'On' : 'Off';
  if (this.checkboxValue === "On") {
      return updateMod('videoembed', 1) ;
  } else {
      return updateMod('videoembed', 0)
  }
})


document.getElementById('extras_btn').addEventListener('change', (e) => {
  this.checkboxValue = e.target.checked ? 'On' : 'Off';
  if (this.checkboxValue === "On") {
      return updateMod('extras', 1) ;
  } else {
      return updateMod('extras', 0)
  }
})


document.getElementById('custom_btn').addEventListener('change', (e) => {
  this.checkboxValue = e.target.checked ? 'On' : 'Off';
  if (this.checkboxValue === "On") {
      return updateMod('custom', 1) ;
  } else {
      return updateMod('custom', 0)
  }
})

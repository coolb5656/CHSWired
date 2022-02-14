$ (document).ready( function() {
  $('#startDate').datepicker({
    "format": "mm-dd-yy",
    "startDate": "1d",
    "endDate": "09-15-2017",
    "keyboardNavigation": false
   });
  });

var items = [];
var names = [];
function addItem() {
  items.push($("#select_items").val());
  names.push($("#select_items option:selected").text())
  $("#ids").val(items);
  $("#items").text(names.join("\r\n"));
  
}
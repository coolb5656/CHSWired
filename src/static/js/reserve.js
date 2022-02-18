var items = [];
var names = [];
function addItem() {
  items.push($("#select_items").val());
  names.push($("#select_items option:selected").text())
  $("#ids").val(items);
  $("#items").text(names.join("\r\n"));
  
}
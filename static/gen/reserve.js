var items = [];
function addItem() {
  items.push($("#select_items").val());
  $("#ids").val(items);
}
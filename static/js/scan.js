$(document).ready(function(){
    var items = [];

    $("#scan").on("click", function (){
        $("#code").focus();
        $('#code').val('');
    });

    $("#code").change(function addItem() {
        $.getJSON($SCRIPT_ROOT + '/checkout/scan', {
            code: $('#code').val()
          }, function(data) {
            if ($("#action").val() == "out") {
                if(!(items.includes(data.id)) && data.status == "In"){
                  items.push(data.id)
                  $("#items").append(data.name +"<br>");
                  $('#ids').val(items);
                }
                else {
                    alert("Item is checked out or not existent!")
                }
            }
            else if ($("#action").val() == "in") {
                if(!(items.includes(data.id)) && data.status == "Out"){
                    items.push(data.id)
                    $("#items").append(data.name + "<br>");
                    $('#ids').val(items);
                  }
                  else {
                    alert("Item is not checked out or not existent!")
                  }
            }
          });
          return false;
    })

    $('form input').keydown(function (e) {
      if (e.keyCode == 13) {
          e.preventDefault();
          $("#code").blur()
          $("#code").focus();
          $('#code').val(''); 
          return false;
      }
  });

  $("#date").change(function changeDate() {
    $.getJSON($SCRIPT_ROOT + '/reservation/check_new_reservation', {
      date: $('#date').val()
    }, function(data) {
          reserved_items = data

          
    });
    return false;
  });

  $("#select_items").change(function addItem() {
    $.getJSON($SCRIPT_ROOT + '/checkout/scan_name', {
        name: $('#select_items').val()
      }, function(data) {
            if(!(items.includes(data.id)) && !(reserved_items.includes(data.id))){
              items.push(data.id)
              $("#items").append(data.name +"<br>");
              $('#ids').val(items);
            }
            else {
                alert("Item is reserved or not existent!")
            }
      });
      return false;
  });
})

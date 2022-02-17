$(document).ready(function(){
$("#scan").on("click", function (){
    $("#code").focus();
    $('#code').val('');
});


$("#position").change(function addpwd() {
    if ($("#position").val() == "Producer") {
        $("#password_field").css( "display", "block" );
    }
});


$('#edit_item_m').on('shown.bs.modal', function () {
    $('#myInput').trigger('focus')
})

$('#edit_item').submit(function(eventObj) {
    return true;
});
})

function addID(id) {
    $('#edit_item').append  (`<input type="hidden" name="id" id="id" value="${id}" /> `);
    console.log(id)
}
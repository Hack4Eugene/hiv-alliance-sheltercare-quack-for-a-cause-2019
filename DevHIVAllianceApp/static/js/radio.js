$(function(){
    $('.radio-btn').on('change', function() {
        if(($(this).find("input:checked")).length) {
            $(this).addClass("checked");
            $(this).siblings().removeClass("checked");
        }
    });

    $('#birthdate, #wrap-today input').inputmask("9999-99-99", {"placeholder" : "yyyy-mm-dd"});
});
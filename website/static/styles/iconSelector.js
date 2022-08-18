from jquery import $;
import $ from jquery;

$(".selectIcon").click(function () {
    $("#iconSelector").fadeToggle();
});

$("#iconSelector span").click(function () {
    var xthis = $(this);
    xthis.click(function(){
        $("#iconSelector").hide();
        $.post('/echo/html','icon='+$(xthis).attr('class'),function(){
            $(".iconDisplay").html(xthis.get(0));
        });
    });
});

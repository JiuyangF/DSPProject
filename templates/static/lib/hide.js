
$(document).ready(function(){
    $("#id_hide").click(function(){
    $("h2").css("background-color","red");
    $("#is_hide").hide(1000,function(){
        $("p").show(1000)
    });
    });

    $("#show").click(function(){
    $("p").show();
    });

    $("#hide").click(function(){
    $("p").hide();
    });

});
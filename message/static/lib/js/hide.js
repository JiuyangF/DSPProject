
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
//    实现文本收起并展开功能，可改变change 按钮的text
     $("#change").click(function(){
    $("p").toggle(2000);
    $("#change").text("收起")
    });
});
/**
 * Created by Administrator on 2017/3/16.
 */
$("#checkAll").click(function () {
    if ($("#checkAll").prop("checked")) {
        $("[name='_dataCheckBox']").prop("checked", 'true');//全选
        $("[name='_dataCheckBox']").each(function () {
            $(this).parent().parent().toggleClass("bg-info");//添加选中样式
        });
    } else {
        $("[name='_dataCheckBox']").removeAttr("checked");//取消全选
        $("[name='_dataCheckBox']").each(function () {
            $(this).parent().parent().toggleClass("bg-info");//取消选中样式
        });
    }
    var a = $("input[name='_dataCheckBox']:checked");
    $("#selected_count").text(a.length);
    if(a.length>0){
        $("#action_buttons :button").attr("disabled",false);
    }else {
        $("#action_buttons :button").attr("disabled",true);
    }
});
//除了表头（第一行）以外所有的行添加click事件.
$("tr").first().nextAll().click(function () {
    //如果没有某个样式则加上，否则去除
    $(this).children().toggleClass("bg-info");
    if ($(this).children().hasClass("bg-info")){//如果有某个样式则表明，这一行已经被选中
        $(this).children().first().children().attr("checked", true);
    } else {                                  //如果没有被选中
        $(this).children().first().children().attr("checked", false);
    }
    var a = $("input[name='_dataCheckBox']:checked");
    $("#selected_count").text(a.length);
    if(a.length>0){
        $("#action_buttons :button").attr("disabled",false);
    }else {
        $("#action_buttons :button").attr("disabled",true);
    }
});


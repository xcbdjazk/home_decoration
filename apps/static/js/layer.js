
function layer_pop(e) {
    e.preventDefault();
    let url = $(this).attr('href') || $(this).attr('url')
    let title = $(this).attr('title') || '信息'
    layer.open({
      type: 2,
      title,
      shadeClose: true,
      shade: 0.8,
      area: ['40%', '60%'],
      content: url //iframe的url
    })
}
$('.pop_layer').click(layer_pop)

$(".delete").click(function (event) {
            event.preventDefault();
            var url = $(this).attr("url") || $(this).attr("href")
            let title = $(this).attr('title') || '信息'
            layer.confirm('确定删除？', {
                title,
                btn: ['确定', '取消'] //按钮

            }, function () {
                $.ajax({
                    url: url,
                    type: "get",
                    success: function (data) {
                        if (data.code === 500) {
                            layer.msg(data.message, {icon: 2});
                        }else {
                            layer.msg('删除成功', {icon: 1});
                            setTimeout(function () {
                                window.location.reload()
                            }, 2000)
                        }
                    }
                })
            }, function () {

            });
        });
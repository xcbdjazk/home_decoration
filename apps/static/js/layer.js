
function layer_pop(e) {
    e.preventDefault();
    let url = $(this).attr('href') || $(this).attr('url')
    let title = $(this).attr('title') || '信息'
    let w = $(this).attr('w') || '40%'
    let h = $(this).attr('h') || '60%'
    let scrollbar = !($(this).attr("scrollbar") === '1')
    console.log(scrollbar)
    layer.open({
      type: 2,
      title,
      shadeClose: true,
      shade: 0.8,
      scrollbar,
      area: [w, h],
      content: url //iframe的url
    })
}
$('.pop_layer').click(layer_pop)

$(".delete").click(function (event) {
            event.preventDefault();
            var url = $(this).attr("url") || $(this).attr("href")
            let title = $(this).attr('title') || '信息'
            let desc = $(this).attr('desc') || '确定删除'

            layer.confirm(desc, {
                title,
                btn: ['确定', '取消'] //按钮

            }, function () {
                $.ajax({
                    url: url,
                    type: "get",
                    success: function (data) {
                        if (data.code !== 200) {
                            layer.msg(data.message, {icon: 2});
                        }else {
                            layer.msg(data.message ||'删除成功', {icon: 1});
                            setTimeout(function () {
                                if(data.data){
                                    if (data.data.url){
                                        window.location.href=data.data.url
                                    }else{
                                        window.location.reload()
                                    }
                                }else{
                                    window.location.reload()
                                }

                            }, 2000)
                        }
                    }
                })
            }, function () {

            });
        });
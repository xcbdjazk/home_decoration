
function layer_pop(e) {
    e.preventDefault();
    let url = $(this).attr('href') || $(this).attr('url')
    let title = $(this).attr('title') || '信息'
    layer.open({
      type: 2,
      title,
      shadeClose: true,
      shade: 0.8,
      area: ['380px', '90%'],
      content: url //iframe的url
    })
}
$('.pop_layer').click(layer_pop)
var $ = require('./jquery.min');

function func_ajax(url, type, param, func) {

	$.ajax({
		url:url,
		type:type,
		data:param,
		success: func,
		error: function (XMLHttpRequest, textStatus, errorThrown) {
		    // 通常 textStatus 和 errorThrown 之中
		    // 只有一个会包含信息
		    console.log(XMLHttpRequest.responseText);
		    this; // 调用本次AJAX请求时传递的options参数
		}
	});

}

$(".form-signin").submit(function () {
	var username = $(".js-username").eq(0).val();
	var pwd = $(".js-pwd").eq(0).val();
	if (username != null && pwd != null) {
		return true;
	}

	return false;
});
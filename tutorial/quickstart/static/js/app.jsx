require('./jquery.min');
var React = require('react');
// require('jquery-browserify');
// var b = require('bootstrap-browserify');
require('react-bootstrap');
// var TimePicker = require('./src');
var DateTimeField = require('react-bootstrap-datetimepicker');

var files = require('./files.jsx');
var Panel = require('./users.jsx');
var func_ajax = require('./public.js');

$(".form-signin").submit(function () {
	var username = $(".js-username").eq(0).val();
	var pwd = $(".js-pwd").eq(0).val();
	if (username != null && pwd != null) {
		return true;
	}

	return false;
});


$(".js-user").click(function () {
	var content = $(".js-content");
	function callback(result) {
		if('redirect' in result) {
			window.location.href=result.redirect;
		}else {
			renderUser(result);
		}
	}
	func_ajax("/user", "GET", "", callback);
});
function renderUser(data) {
	React.render(
		<Panel users={data.Users} positions={data.Positions} page={data.pageNum}>
		</Panel>,
		document.getElementById('js-content')
	);
}



$("#files").on('click',function() {
	renderFile('test');
});


function renderFile(data) {
	files(data);
}
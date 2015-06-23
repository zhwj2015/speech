require('./jquery.min');
var React = require('react');
// require('jquery-browserify');
// var b = require('bootstrap-browserify');
require('react-bootstrap');
// var TimePicker = require('./src');
var DateTimeField = require('react-bootstrap-datetimepicker');
var data = null;

/**
* ajax before send
*
*/
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(function() {
    var csrftoken = getCookie('csrftoken');
   
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});











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



$(".js-user").click(function () {
	var content = $(".js-content");
	function callback(result) {
		renderUser(result);
	}
	func_ajax("/user", "GET", "", callback);
});



/**
	UI 
*/
var Pheader = React.createClass({
	render: function () {
		var click = this.props.onClick?this.props.onClick:null;
		var count = this.props.count? this.props.count:0;
		return (
			<div className="panel-heading">
				职工表
				<div className="pull-right">
					<a className="glyphicon glyphicon-plus-sign" href="javascript:void(0)" onClick={click}></a>
					<span className="badge">{count}</span>
				</div>
			</div>
			)
	}
});


var Umodal = React.createClass({
	getInitialState: function() {
		var user = Object();
		var date = new Date();
		user.user_id = '';
		user.name = '';
		user.sex = 1;
		user.age = '';
		birthday = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
		user.birthday = birthday;
		user.position = '';
		user.score = '';
		return {user:user, positions: []}//{user_id:'',name:'',sex:'',age:'',birthday:'',position:'',score:'',positions:[]}
	},
	initUserState: function () {
		var user = Object();
		var date = new Date();
		user.user_id = '';
		user.name = '';
		user.sex = 1;
		user.age = '';
		birthday = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
		user.birthday = birthday;
		user.position = '';
		user.score = '';
		return user;
	},
	setKeyValue: function(key, user, value){
		if (user == '') {
			user = Object();
		}
		switch(key) {
			case 'user_id':
				  user.user_id = value;
				  break;
			case 'name':
				  user.name = value;
				  break;
			case 'sex':
				  user.sex = value;
				  break;
			case 'age':
				  user.age = value;
				  break;
			case 'birthday':
				  var date = new Date();
				  date.setTime(value);
				  user.birthday = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
				  break;
			case 'position':
				  var p = null;
				  this.state.positions.map(function(position) {
				  	if (position.id == value) {
				  		p = position;
				  	}
				  })
				  user.position = p;
				  break;
			case 'score':
				  user.score = value;
				  break;
		}
		return user;
		
	},
	setStateValue: function(data) {
		if(data!=null) {
			this.setState({user: data});
		}else {
			this.setState({user: ''});
		}
		
	},
	onChange: function (e) {
		var field = e.target.getAttribute('data-field');
		var value = e.target.value;
		var user = this.state.user;
		user = this.setKeyValue(field, user, value);
		this.setState({user: user});
	},
	onTimeChange: function(e) {
		var user = this.state.user;
		user = this.setKeyValue('birthday', user, e);
		this.setState({user: user});
	},
	componentWillMount: function() {
		var data = this.props.data_users;
		if (data == '' || data == null) {
			data = this.initUserState();
		}
		// this.setState({user: data});
		this.setStateValue(data);
		var pData = this.props.data_positions;
		this.setState({positions: pData});
	},
	componentWillReceiveProps: function(nextProps) {
		var data = nextProps.data_users;
		if (data == '' || data == null) {
			data = this.initUserState();
		}
		// this.setState({user: data});
		this.setStateValue(data);
		var pData = nextProps.data_positions;
		this.setState({positions: pData});
		
	},
	callback: function(result) {
		if (!('False' in result && result.False == false)) {
			this.setState({user: result});
			this.props.onCallBack(result);
			$('#show_modal').modal('hide');
		}
		
	},
	handleSubmit: function() {
		var user = this.state.user;
		var date = new Date(user.birthday);
		user.birthday = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
		if(user.position == '') {
			user.position = this.state.positions[0];
		}
		var arrParam = {"csrfmiddlewaretoken": window.csrftoken, "data": user}
		var method = this.props.method;
		if(method == 'update') {
			func_ajax('/update', 'POST', arrParam, this.callback);
		}else if (method == 'add'){
			func_ajax('/add', 'POST', arrParam, this.callback);
		}

	},
	

	render: function ()  {
		var that = this;
		var sselect = this.state.positions.map(function(position) {

			var dom = null;
			if(that.state.position == position) {
				dom = <option value={position.id} selected >{position.name}</option>;	
			}else {
				dom = <option value={position.id}>{position.name}</option>;
			}
			return (
				dom
				)
		});
		
		var user = this.state.user;
		var user_id, name, sex, age, birthday, position, score ;
		if(user != '') {
			user_id = user.user_id;
			name = user.name;
			sex = user.sex;
			age = user.age;
			date = new Date(user.birthday);
			birthday = date.getTime().toString();
			position = user.position;
			score = user.score;
		}else {
			user_id = '';
			name = '';
			sex = 1;
			// user = this.setStateValue('sex', user, 1);
			age = '';
			date = new Date();
			birthday = date.getTime().toString();
			// user = this.setStateValue('birthday', user, date);
			position = '';
			score = 0;
		}
		return (
			<div className="modal" id="show_modal" tabIndex="-1" role="dialog" aria-labelledby="show_title" aria-hidden="true">
				<div className="modal-dialog">
					<div className="modal-content">
						<div className="modal-header">
							<button type="button" className="close" data-dismiss="modal" aria-hidden="true">
								&times;
							</button>
							<h4 className="modal-title" id="show_title">
								职工信息
							</h4>
						</div>
						<div className="modal-body">
							<div className="form-horizontal" role="form" >
							   <div className="form-group">
							      <label htmlFor="user_id" className="col-sm-2 control-label">职工号</label>
							      <div className="col-sm-10">
							         <input type="text" className="form-control" id="user_id" readOnly name="user_id" data-field="user_id"
							            placeholder="自动生成" value={user_id}/>
							      </div>
							   </div>
							   <div className="form-group">
							      <label htmlFor="name" className="col-sm-2 control-label">姓名</label>
							      <div className="col-sm-10">
							         <input type="text" className="form-control" id="name" name="name" data-field="name" onChange={this.onChange}
							            placeholder="请输入姓名" value={name}/>
							      </div>
							   </div>
							   <div className="form-group">
							      <label htmlFor="lastname" className="col-sm-2 control-label">性别</label>
							      <div className="col-sm-10">
							         <label className="radio-inline">
							           <input type="radio" className="col-sm-5" name="sex" id="inlineRadio1" value="1" data-field="sex" onChange={this.onChange} checked={sex==1?true:false } /> 男
							         </label>
							         <label className="radio-inline">
							           <input type="radio" className="col-sm-5" name="sex" id="inlineRadio2" value="0" data-field="sex" onChange={this.onChange} checked={sex==0?true:false}/> 女
							         </label>
							      </div>
							   </div>
							   <div className="form-group">
							      <label htmlFor="age" className="col-sm-2 control-label">年龄</label>
							      <div className="col-sm-10">
							         <input type="text" className="form-control" id="age" name="age" data-field="age" onChange={this.onChange}
							            placeholder="请输入年龄" value={age}/>
							      </div>
							   </div>
							   <div className="form-group">
							      <label htmlFor="age" className="col-sm-2 control-label">出生年月</label>
							      <div className="col-sm-10">
							         <DateTimeField ref="birthday" data-field="birthday" dateTime={birthday} inputFormat="MM-DD-YYYY" onChange={this.onTimeChange}/>
							      </div>
							   </div>
							   
							   <div className="form-group">
							      <label htmlFor="position" className="col-sm-2 control-label">岗位</label>
								  <div className="col-sm-10">
								      <select className="form-control" name="position" data-field="position" id="position" onChange={this.onChange}>
								        {sselect}
								      </select>
							      </div>


							   </div>
							     <div className="form-group">
							      <label htmlFor="score" className="col-sm-2 control-label">评分</label>
							      <div className="col-sm-10">
							         <input type="text" className="form-control" id="score" name="score" data-field="score" onChange={this.onChange}
							            placeholder="请输入评分" value={score}/>
							      </div>
							   </div>
							   <div className="modal-footer">
		   							<button type="button" className="btn btn-default" data-dismiss="modal">关闭</button>
		   							<button type="submit" className="btn btn-primary" onClick={this.handleSubmit}>提交</button>
		   						</div>
							</div>
						</div>
						
					</div>
				</div>

			</div>
			);
	}

});


/**
* 表格主体
*
*/
var Panel = React.createClass({
	getInitialState: function() {
	    return {user: null, positions:[],users:[], method:'update'};
	},
	trClick: function (e) {
		var index = e.target.getAttribute('data-index');
		var users = this.props.users;
		var data = users[index];
		this.setState({user:data})
		this.setState({method: 'update'});
		$('#show_modal').modal('show');
	},
	componentWillMount:function() {
		var users = this.props.users;
		var positions = this.props.positions;
		this.setState({positions:positions});
		this.setState({users:users});
	},

	componentWillReceiveProps: function(nextProps) {
		var users = nextProps.users;
		var positions = nextProps.positions;
		this.setState({positions:positions});
		this.setState({users:users});
	},
	callback: function(data) {
		var users = this.state.users;
		var arrUsers = [];
		var flag = 0;
		users.map(function(user) {
			if(user.user_id == data.user_id) {
				user.user_id = data.user_id;
				user.name = data.name;
				user.sex = data.sex;
				user.age = data.age;
				user.birthday = data.birthday;
				user.position = data.position;
				user.score = data.score;
				arrUsers = arrUsers.concat(user);
				flag = 1;
			}else {
				arrUsers = arrUsers.concat(user);
			}

		});
		if (flag == 0) {
			arrUsers = arrUsers.concat(data);
		}
		this.setState({users:arrUsers});
	},
	onClick: function() {
		this.setState({user:''});
		this.setState({method:'add'});
		$('#show_modal').modal('show');
	},
	render: function() {
		var that = this;
		var users = that.state.users;
		var content =  users.map(function(user,index) {
							date = new Date(user.birthday);
							birthday = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate();
							return (
								<tr onClick={that.trClick} style={{textAlign:'center'}}>
									<th data-index={index}>{ user.user_id }</th>
									<th data-index={index}>{ user.name }</th>
									<th data-index={index}>{ user.sex==1?'男':'女' }</th>
									<th data-index={index}>{ user.age }</th>
									<th data-index={index}>{ birthday }</th>
									<th data-index={index}>{ user.position.name }</th>
									<th data-index={index}>{ user.score }</th>
								</tr>
							)
						});
		return (
			<div className="panel panel-default">
				<Pheader count={2} onClick={this.onClick} />
				<div className="panel-body js-content">
					<table className="table table-hover">
						<thead>
							<th>职工号</th>
							<th>姓名</th>
							<th>性别</th>
							<th>年龄</th>
							<th>出生年月</th>
							<th>职位</th>
							<th>评分</th>
						</thead>
						<tbody>
							{content}
						</tbody>
					</table>
					<Umodal data_users={this.state.user} data_positions={this.state.positions} onCallBack={this.callback} method={this.state.method}/>
				</div>
			</div>

			)
	}
});

// var Panel = React.createClass({
	
// 	render: function () {

// 		var count = this.props.count;
// 		var users = this.props.users;
// 		var positions = this.props.positions;
// 		return (
// 				<Pbody users={users} positions={positions}/>
// 			);
// 	}
// });


function renderUser(data) {
	React.render(
		<Panel count={2} users={data.Users} positions={data.Positions}>
		</Panel>,
		document.getElementById('js-content')
	);
}
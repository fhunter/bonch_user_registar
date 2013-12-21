var valid_data=false;
function submit_user() {
	check_validity();
}

function toLatin(str) {
	//Transliterates string to lowercase latin
	return str.toLowerCase();
}

function generate_username() {
	//Generates username from familyname and name
	//Generates password
	var last_name = document.getElementsByName( "last_name")[0].value.trim();
	var first_name = document.getElementsByName( "first_name")[0].value.trim();
	var patronimic = document.getElementsByName( "patronimic")[0].value.trim();
	var username = "";
	var password = "";
	username = toLatin(last_name) + toLatin(first_name).charAt(0) + toLatin(patronimic).charAt(0);
	password = "blah";
	document.getElementsByName( "username" )[0].value = username;
	document.getElementsByName( "initialpassword" )[0].value = password;
}
function check_validity() {
	var local_valid = true;
	var text = "";
	var fail = '<img src="fail.png" />';
	var ok = '<img src="ok.png" />';
	var preamble = "<div class=\"field_container\">";
	var post = "</div>";
	var elements = new Array();
	elements.push(new Array("last_name","фамилия"));
	elements.push(new Array("first_name","имя"));
	elements.push(new Array("patronimic","отчество"));
	elements.push(new Array("studentnumber","номер студенческого билета"));
	elements.push(new Array("username","имя пользователя"));
	elements.push(new Array("initialpassword","начальный пароль"));
	for(i=0;i<elements.length;i++){
		//Проверка полей на пустоту
		if(document.getElementsByName( elements[i][0] )[0].value.trim() == ""){
			text += preamble + fail + "Пустое поле " + elements[i][1] + post;
			local_valid = false;
		}else{
			text += preamble +   ok + elements[i][1] + post;
		}
	}
	//Добавить проверку поля username на повторяемость
	//Добавить проверку поля номер студбилета на число
	//Добавить проверку поля номер студбилета на дублируемость
	document.getElementById("check_results").innerHTML = text;

	valid_data = local_valid;
}

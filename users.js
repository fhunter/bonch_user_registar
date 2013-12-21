var valid_data=false;
function submit_user() {
	check_validity();
}
function check_validity() {
	var local_valid = true;
	var text = "";
	var fail = '<img src="fail.svg" />';
	var ok = '<img src="ok.svg" />';
	var preamble = "";
	var post = "";
	var elements = new Array();
	elements.push(new Array("last_name","Фамилия"));
	elements.push(new Array("first_name","Имя"));
	elements.push(new Array("patronimic","Отчество"));
	elements.push(new Array("studentnumber","Номер студенческого билета"));
	elements.push(new Array("username","имя пользователя"));
	elements.push(new Array("initial_password","начальный пароль"));
	for(i=0;i<elements.length;i++){
		//Проверка фамилии на пустоту 
		if(document.getElementsByName( elements[i][0] )[0].value == ""){
			text += preamble + fail + "Пустое поле " + elements[i][1] + post;
			local_valid = false;
		}else{
			text += preamble +   ok + elements[i][1] + post;
		}
//		if(document.getElementsByName( "first_name")[0].value == ""){
//			text += "Empty first name";
//			local_valid = false;
//		}
//		if(document.getElementsByName( "studentnumber")[0].value == ""){
//			text += "Empty student number";
//			local_valid = false;
//		}
//		if(document.getElementsByName( "studentnumber")[0].value == ""){
//			text += "Not a number";
//			local_valid = false;
//		}
//		if(document.getElementsByName( "username")[0].value == ""){
//			text += "Empty username";
//			local_valid = false;
//		}
//		if(document.getElementsByName( "username")[0].value == ""){
//			text += "Invalid username. ";
//			local_valid = false;
//		}
//		if(document.getElementsByName( "initialpassword")[0].value == ""){
//			text += "Empty initial password. ";
//			local_valid = false;
//		}
	}
	document.getElementById("check_results").innerHTML = text;

	valid_data = local_valid;
}

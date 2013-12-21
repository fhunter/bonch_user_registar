var valid_data=false;
function submit_user() {
	check_validity();
}
function generate_username() {
	//Generates username from familyname and name
	//Generates password
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

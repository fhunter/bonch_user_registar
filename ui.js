function div_toggle(div_id){
  var t=document.getElementById(div_id);
  for(i=0;i<t.parentElement.getElementsByTagName("div").length;i++){
    p=t.parentElement.getElementsByTagName("div")[i];
    if(p.parentElement.id == t.parentElement.id ){
      if(p.id==div_id){
	p.style.display ="inline";
      }else{
	p.style.display ="none";
      }
    }
  }
}

var valid_data=false;
function submit_user() {
	//FIXME: add sending data to server
	check_validity();
}

function isANumber(str) {
	var result=true;
	var numbers="0123456789";
	for(i = 0; i<str.length;i++) {
		if(numbers.indexOf(str.charAt(i))==-1){
			result = false;
		};
	};
	return result;
}

function toLatin(str) {
	//Transliterates string to lowercase latin
	var A = {};
	var whitelist = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщьыъэюя01234567890_";
	var result = '';
	
	A["ё"]="yo";A["й"]="j";A["ц"]="ts";A["у"]="u";A["к"]="k";
	A["е"]="e";A["н"]="n";A["г"]="g";A["ш"]="sh";A["щ"]="sch";
	A["з"]="z";A["х"]="h";A["ъ"]="_";A["ф"]="f";A["ы"]="y";
	A["в"]="v";A["а"]="a";A["п"]="p";A["р"]="r";A["о"]="o";
	A["л"]="l";A["д"]="d";A["ж"]="zh";A["э"]="e";A["я"]="ya";
	A["ч"]="ch";A["с"]="s";A["м"]="m";A["и"]="i";A["т"]="t";
	A["ь"]="_";A["б"]="b";A["ю"]="yu";A[" "]="_";

	str=str.toLowerCase();
	var str1 = "";
	for(i = 0; i < str.length; i++) {
		if(whitelist.indexOf(str.charAt(i))==-1){
			//Cleanup - replace everything unknown with _
			str1+= '_';
		}else{
			str1+=str.charAt(i);
		}
	}
	str=str1;
	str1 = str.charAt(0);
	for(i=1; i < str.length; i++) {
		//remove duplicate '_'
		if(!((str.charAt(i-1)=='_') && (str.charAt(i)=='_'))){
			str1 += str.charAt(i);
		}
	}
	str=str1;
	for(i = 0; i < str.length; i++) {
		c = str.charAt(i);
		//Russian to latin
		result += A[c] || c;
	}

	return result;
}

function generate_username() {
	//Generates username from familyname and name
	//Generates password
	//FIXME: add password generation
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
	if(!isANumber(document.getElementsByName("studentnumber")[0].value.trim())){
		text += preamble + fail + "Нечисловые данные в поле " + "номер студенческого билета" + post;
		local_valid = false;
	}
	//Добавить проверку поля номер студбилета на дублируемость
	document.getElementById("check_results").innerHTML = text;

	valid_data = local_valid;
}

function fetch_groups(){
	var jsonHttp = null;
	jsonHttp = new XMLHttpRequest();
	jsonHttp.open( "GET", "ui.py?query=group", false );
	jsonHttp.send( null );
	var myobject = JSON.parse(jsonHttp.responseText);
	var text = "";
	for(i=0;i<myobject.groups.length;i++){
		text += "<option value=\"" + myobject.groups[i][0] + "\">" + myobject.groups[i][1] + "</option>";
	};
	document.getElementById("groupselectorid").innerHTML = text;
}

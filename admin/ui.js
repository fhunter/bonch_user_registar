function div_toggle(div_id){
  	var t=document.getElementById(div_id);
	for(i=0;i<t.parentElement.getElementsByTagName("div").length;i++){
	  p=t.parentElement.getElementsByTagName("div")[i];
	  if(p.id==div_id){
	    p.style.display ="inline";
	  }else{
	    p.style.display ="none";
	  }
	}
}



// Hide the div
function hide_me(id) {
	document.getElementById(id).style.display = 'none';
}

function toggle_visibility(msgid){

	visible = document.getElementById(msgid).style.display;

	if(visible == 'none'){
		document.getElementById(msgid).style.display = 'block';
	}
	else{
		document.getElementById(msgid).style.display = 'none';
	}
	
}

// Function to validate reply and 
// call the appropriate view by generating the url
function send_reply(subject, msgid, rec){
	
	message = document.getElementById(msgid).getElementsByTagName('textarea')[0].value;
	
	// Check that message is not empty
	if(message==""){
		alert("Empty message");
	}
	
	// Check whether any of the parameters are empty
	else if(subject =="" || msgid=="" || rec==""){
		alert("One of more missing parameters!");
	}
	// If basic validation is passed
	else{
	// Create path;
	path = "/reply/" + subject + "/" + msgid + "/" + rec + "/" + message;
	
	//Redirect
	window.location.replace(path);
	}
}






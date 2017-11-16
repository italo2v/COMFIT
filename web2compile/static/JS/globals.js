/*
"""This file contains code for use with "Web2CompileCloud",
by Italo C. Brito, Geovane Mattos, Marina Vianna, Claudio C. Miceli available from labnet.nce.ufrj.br

Copyright 2015 - UFRJ
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""
*/


var editor = undefined;

//configure a prefix route
var route = '/web2compile/';


//getting url variables
var params = {};
if (location.search) {
    var parts = location.search.substring(1).split('&');

    for (var i = 0; i < parts.length; i++) {
        var nv = parts[i].split('=');
        if (!nv[0]) continue;
        params[nv[0]] = nv[1] || true;
    }
}


//adjusts the size os components, starts the ace editor
$( document ).ready(function() {

	$('#openOrion').click(
		function(){
			window.open('/edit/edit.html', 'orionEditor');
		}
	);
	
	$('#getStatus').click(
		function(){
			//submitExperiment();
			id = $('#experimentId').val();
			statusExperiment(id);
		}
	);
	
	$('#compile').click(
		function(){
			compileMicaz();
		}
	);


	h = window.innerHeight;
	topo = 8+28+5+30;
	if(document.getElementById('buttons'))
		topo += 42;
	consoleh = 190;
	h = h-topo;
	
	//adjusting the sizes os ace editor, list of files or experiments
	$('#coojaGUI').css('display', 'none');
	$('#coojaGUI').css('height', h-50);
	$('#console').css('display', 'none');
	$('#console').css('height', '150');
	$('#files').css('width', '100%');
	$('#files').css('height', h);
	$('#files').css('float', 'left');
	$('#experiments').css('height', h);
	$('#edit').css('width', '70%');
	$('#edit').css('float', 'right');
	$('#edit').css('height', h);
	$('#editor').css('height', h-40);
	$('#list').css('width', '100%');
	$('#maxsizelist').css('height', h-10);
	$('#edit').css('display', 'none');

	//ace editor
	if(document.getElementById('editor')){
		editor = ace.edit("editor");
		editor.setTheme("ace/theme/merbivore");
		editor.getSession().setMode("ace/mode/python");
		editor.setHighlightActiveLine(true);
		editor.$blockScrolling = Infinity;
		editor.getSession().on('change', function(e) {
    		$('#changed').html('*');
		});
		editor.commands.addCommand({
		    name: 'save',
		    bindKey: {win: 'Ctrl-S',  mac: 'Command-S'},
		    exec: function(editor) {
			saveFile();
		    },
		    readOnly: false // false if this command should not apply in readOnly mode
		});

	}
	
	listProjects();
});

//refresh the project list
function listProjects(){
	$('#list').html('');
	var formData = new FormData();
	formData.append('user', params.user);
	$.ajax({
            type: 'POST',
            url: route+'listProjects',
    	    data: formData,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(result) {
				list = eval(result);
				n=0;
				for(i=0;i<list.length;i++){

					project = list[i];
					div = $('<div id="project-'+project.replace(" ", "---")+'">')
					.addClass('project');
					$('<span>').addClass('projectName').html(project).click(function(){openProject(this)}).appendTo(div);
					$('<button>').addClass('small').html('Compile to TOSSIM').click(function(){compileMicaz(this)}).appendTo(div);

					$('#list').append(div);
					n+=1;

				}
            },
    });
	
}

//refresh the resources list of a project or close it
function openProject(project){
	if( $(project).parent().find('div').length){ //close the project
		$(project).parent().find('div').remove();
		return;
	}
	projectname = $(project).html();
	var formData = new FormData();
	formData.append('projectname', projectname);
	formData.append('user', params.user);
	$.ajax({
            type: 'POST',
            url: route+'openProject',
    	    data: formData,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(result) {
				list = eval(result);
				for(i=0;i<list.length;i++){

					path = list[i].path;
					type = list[i].type;

					if(type == 'file'){
					  file = $('<div>').addClass('item');
					  $('<span>').addClass('itemName').html(path).click(function(){openFile(this)}).appendTo(file);

					  $('#project-'+projectname.replace(" ", "---")).append(file);
					}
					else if(type == 'folder'){/*
					  folders = path.split('/')
					  for(f=0;f<folders.length;f++)
					    if( ! $('#'+projectname+'-'+path).length ){
					      folder = $('<div id="'+projectname+'-'+path+'">').addClass('folder');
					      button = $('<button id="btn-'+projectname+'-'+path+'">').html('>')
						.attr('onClick', 'openFolder("'+projectname+'-'+path+'");').addClass('small');
					      folder.append(button);
					      folder.html( folder.html()+'&nbsp;'+folders[f] );
					      if( f >= 1 || $('#'+projectname+'-'+path).length ){
					        folder.attr('style', 'display:none;');
						last = path.split(folders[f])[0]
					        $('#'+projectname+'-'+last).append(folder);
					      }else
					        $('#project-'+projectname).append(folder);
					    }*/
					}

					split = path.split('.')
					ext = split[split.length-1].toLowerCase();
					if(ext == 'py'){
						$('<button>').click(
							function(){
								confirmTime(this);
							}
						).addClass("small").html("Execute").appendTo(file);
					}
					else if(ext == 'csc'){
						$('<button>').click(
							function(){
								confirmTime(this);
							}
						).addClass("small").html("Simulate COOJA").appendTo(file);
					}

				}
            },
    });
	
}

//open the file
function openFile(resource){
	path = $(resource).html();
	projectname = $(resource).parent().parent().find('span').html();
	var formData = new FormData();
	formData.append('path', path);
	formData.append('projectname', projectname);
	formData.append('user', params.user);
	$.ajax({
            type: 'POST',
            url: route+'openFile',
    	    data: formData,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(result) {
				if($('#changed').html() == '*'){
					if(!confirma('Unsaved changes', 'Are you sure you want to close the actual file? All the changes will be lost.', 'hide()'))
						return false;
				}
				
				filename = path.split('/').pop();
				editor.setValue(result);
				split = filename.split('.');
				ext = split[split.length-1].toLowerCase();
				$('#legend').html('Editor');
				$('#editor').css('display', 'block');
				if(ext == 'py'){
					editor.getSession().setMode("ace/mode/python");
				}else if(ext == 'c'){
					editor.getSession().setMode("ace/mode/c_cpp");
				}else if(ext == 'nc'){
					editor.getSession().setMode("ace/mode/c_cpp");
				}else if(ext == 'java'){
					editor.getSession().setMode("ace/mode/java");
				}else if (ext == 'csc'){
					editor.getSession().setMode("ace/mode/xml");
					//showCoojaGUI(params.user, projectname, path);
				}
				$('#file_editing').html(filename);
				$('#filePath').html(path);
				$('#projectName').html(projectname);
				if( $('#edit').css('display') == 'none')
				  showEdit();
				$('#changed').html('');
            },
    });
	
}


//save changes overwriting the file
function saveFile(){
	var formData = new FormData();
	filePath = $('#filePath').html();
	projectname = $('#projectName').html();
	formData.append('path', filePath);
	formData.append('projectname', projectname);
	formData.append('user', params.user);
	formData.append('content', editor.getValue());
	       $.ajax({
            type: 'POST',
            url: route+'saveFile',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(result) {
				$('#changed').html('');
				if(result == "TRUE")
					alerta('Success', 'File saved successfully!');
				else
					alerta('Error', 'Error while saving the file!');
            },
        });
}

//ask if you really want to close the file if you have not saved changes
function closeFile(){
	if($('#changed').html() == '*'){
	  confirma('Unsaved changes', 'Are you sure you want to close the file? All the changes will be lost.', 'hide()');
    }else{
		hide();
    }
}

//compile the app for micaz simulation with tossim
function compileMicaz(project){
	projectname = $(project).parent().find('span.projectName').html();
	user = params.user;
	dir = './projects/'+user+'/'+projectname;
	shellexec(function(output){
		openConsole();
		$('#Console-log').html(output);
	}, 'make --directory='+dir+' -I '+dir+' micaz sim', 'local', projectname);
}

//execute a command in shell and shows in console the return
function shellexec(handleData, cmd, local, project){
	local = local || 'local';
	formData = new FormData();
	formData.append('cmd', cmd);
	formData.append('user', params.user);
	formData.append('project', project);
	showProcessing();
	setTimeout(function(){
			$.ajax({
		            type: 'POST',
		            url: route+local+'exec',
		            contentType: false,
					data: formData,
		            cache: false,
		            processData: false,
		            async: false,
		            success: function(result) {
						$('#processing').css('display', 'none');
						handleData(result);
		            }
		    });
	}, 100);

}

//shows the Cooja GUI
function showCoojaGUI(user, projectname, path){
	$('#legend').html('Cooja: The Contiki Network Simulator');
	$('#editor').css('display', 'none');
	$('#coojaGUI').css('display', 'block');
	$('#coojaGUI').attr('src', 'static/cooja.html?user='+user+'&projectname='+projectname+'&path='+path);
}

//shows the edit window
function showEdit(){
	if($('#edit').css('display') == 'none'){
		$('#edit').css('width', '0');
		$('#edit').css('display', 'block');
		$('#files').animate({ width: '30%' }, 400 );
		$('#edit').animate({ width: '70%' }, 400 );
	}
}

//shows the dialog processing...
function showProcessing(){
	createElement('processing');
	$('#processing').css('display', 'block');
	$('#processing').css('background-image', 'linear-gradient(to bottom,#337ab7 0,#265a88 100%)');
	$('#processing').css('top', $( window ).height()/2-40);
	$('#processing').css('left', $( window ).width()/2-100);
	$('#processing').html('<center><font color=black>Processing...</font><BR><img src="static/images/load.gif"></center>');
}

//close the edit window
function hide(){
	editor.setValue('');
	$('#file_editing').html('');
	$('#edit').css('display', 'none');
	$('#files').animate({ width: '100%' }, 400 );
	$('#edit').animate({ width: '0' }, 400 );
	window.setTimeout("$('#edit').css('display', 'none');", 500);
	$('#changed').html('');
}


//confirms the execution time
function confirmTime(button){
	minutes = 10;
  	confirma('Time limit',
		'Make sure you code do not have an infinite loop, we set the time limit to '+minutes+' minutes!',
		function(){executeFile(button, minutes)}
	);
}

//execute the file and shows the result in console
function executeFile(button, minutes){
	path = $(button).parent().find('span.itemName').html();
	project = $(button).parent().parent().find('span.projectName').html();
	var formData = new FormData();
	formData.append('path', path);
	formData.append('minutes', minutes);
	formData.append('project', project);
	formData.append('user', params.user);
	showProcessing();
	setTimeout(function(){
		
	$.ajax({
    type: 'POST',
    url: route+'execute',
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    async: false,
    success: function(result) {
		$('#Console-log').html('');
		$('#Console-log').append(result);
		openConsole();
		$('#processing').css('display', 'none');
	}
	});
	
	}, 100);
}

//open the console
function openConsole(){
	if($('#console').css('display') != 'block'){
		h -= consoleh;
		$('#console').css('display', 'block');
		if(document.getElementById('edit')){
		$('#console').animate({ 'margin-top': h+20 }, 400 );
			$('#edit').animate({ height: h }, 400 );
			$('#editor').animate({ height: h-40 }, 400 );
			$('#maxsizelist').animate({ height: h-30 }, 400 );
			$('#files').animate({ height: h }, 400 );
		}
		if(document.getElementById('experiments')){
			$('#console').animate({ 'margin-top': 10 }, 400 );
			$('#experiments').animate({ height: h }, 400 );
		}
	}
}

//close the console
function closeConsole(){
	if($('#console').css('display') == 'block'){
		h += consoleh;
		$('#console').animate({ 'margin-top': h+20 }, 400 );
		if(document.getElementById('edit')){
			$('#edit').animate({ height: h }, 400 );
			$('#editor').animate({ height: h-40 }, 400 );
			$('#maxsizelist').animate({ height: h-10 }, 400 );
			$('#files').animate({ height: h }, 400 );
		}
		if(document.getElementById('experiments')){
			$('#experiments').animate({ height: h }, 400 );
		}
		$('#console').css('display', 'none');
	}
}

//alert the user with a message
function alerta(title, msg){

	createElement('alert');
	$('#alert').html(msg);
	$( "#alert" ).dialog({
		autoOpen: false,
		width: 400,
		title: title,
		buttons: [
			{
				text: "OK",
				click: function() {
					$( this ).dialog( "close" );
					$( this ).remove();
				}
			}
		],
    	open: function(event, ui){
   		 setTimeout("$('#alert').dialog('close')",3000);
   	 	}
	});
	$('#alert').dialog("open");
}

//show a dialog to the user with a message to confirm or cancel
function confirma(title, msg, func){
	
	createElement('confirma');
	$('#confirma').html(msg);
	$( "#confirma" ).dialog({
		autoOpen: false,
		width: 400,
		title: title,
		buttons: [
			{
				text: "OK",
				click: function() {
					$( this ).dialog( "close" );
					$( this ).remove();
					func();
				}
			},
			{
				text: "Cancel",
				click: function() {
					$( this ).dialog( "close" );
					$( this ).remove();
					return false;
				}
			}
		]
	});
	$('#confirma').dialog("open");
}

//create a div element in the body with display:none
function createElement(name){
	div = document.getElementById(name);
	if(div == undefined){
		div = document.createElement('div');
		div.setAttribute('id', name);
		div.setAttribute('style', 'display:none');
		body = document.getElementsByTagName('body');
		body[0].appendChild(div);
	}
	return div;
}




//ask if you really wanto to delete the file - NotUsed
/*function deletar(filename){
	file_editing = $('#file_editing').html();
	if(file_editing == filename){
		if($('#changed').html() == '*')
			confirma('Unsaved changes', 'Are you sure you want to delete the file '+filename+'? All the changes will be lost.', 'del("'+filename+'");hide();');
		else
			confirma('Delete File', 'Are you sure you want to delete the file '+filename+'? ', 'del("'+filename+'");hide();');
	}else
		confirma('Delete File', 'Are you sure you want to delete the file '+filename+'? ', 'del("'+filename+'");hide();');
}*/



//delete the file of the folder and refresh the list - NotUsed
/*function del(filename){
	var formData = new FormData();
	formData.append('filename', filename);
	$.ajax({
    type: 'POST',
    url: route+'delete',
    data: formData,
    contentType: false,
    cache: false,
    processData: false,
    async: false,
    success: function(result) {
		if (result == 'TRUE'){
			file_editing = $('#file_editing').html();
			//Dropzone.prototype.removeFilename(filename);
			$('span:contains(\''+filename+'\')').parent().parent().parent().remove(); //remove from dropzone
			if(filename == file_editing) //close ace editor if the file editing is the file deleted
				hide();
			if ($('.dz-preview').html() == undefined) //show "Drop files here to upload"
				$(".dz-message").css('display', 'block');
			alerta('Success', 'File '+filename+' deleted successfully!');
		}else
			alerta('Error', 'Error deleting file '+filename+'!');
		
    },
	});
	listProjects();
}*/

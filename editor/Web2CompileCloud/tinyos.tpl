<!--
"""This file contains code for use with "Web2CompileCloud",
by Italo C. Brito, Geovane Mattos, Marina Vianna, Claudio C. Miceli available from labnet.nce.ufrj.br

Copyright 2015 - UFRJ
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""
-->
<head>
<script src="static/JS/jquery.js" type="text/javascript" charset=utf-8></script>
<title>Web2CompileCloud</title>
<link rel="stylesheet" type="text/css" href="static/css/style.css">
<link rel="stylesheet" type="text/css" href="static/css/dropzone.css">
<link rel="stylesheet" type="text/css" href="static/css/jquery-ui.css">
  <script src="static/JS/globals.js" type="text/javascript" charset="utf-8"></script>
  <script src="static/JS/dropzone.js" type="text/javascript" charset="utf-8"></script>
  <script src="static/JS/jquery-ui.js" type="text/javascript" charset="utf-8"></script>
  <script src="static/src-min/ace.js" type="text/javascript" charset="utf-8"></script>
</head>
	
<body bgcolor=#E5E5E5>

	<div align="center"> 
		<b><font size=5 color=#2720E9 face=Arial>Web2CompileCloud</font></b>
	</div>
	
	<div align=center id="buttons">
		<button type="button" id="openUpload">Open upload box</button>
		<form action="" method="post" class="dropzone" id="my-awesome-dropzone" enctype="multipart/form-data" style="width:600px; overflow-y: scroll;">
  		<input type="file" name="upload" id="upload"  multiple style="display:none;"/>
  			<!--<div class="dz-preview dz-file-preview">
  		  	  <div class="dz-details">
  				<div class="dz-filename"><span data-dz-name></span></div>
  			  	<div class="dz-size" data-dz-size></div>
  			  	<img data-dz-thumbnail />
  		  	  </div>
 			  <div class="dz-progress"><span class="dz-upload" data-dz-uploadprogress></span></div>
 			  <div class="dz-success-mark"><span>✔</span></div>
 			  <div class="dz-error-mark"><span>✘</span></div>
  			  <div class="dz-error-message"><span data-dz-errormessage></span></div>
		  	</div>-->
			<!-- <input type="button" value="Upload" id="enviar"> <div id="abaixo"></div> -->
		</form>

	</div>
	
	<div style="float:left;margin-top:5px;" id="files">
		<fieldset style="height:100%;">
			<legend> <b>Files uploaded / <button id="compile" class="small">Compile</button></legend></b>
			<div style="overflow-y: scroll;" id="maxsizelist">
				<div id="uploadedList"></div>
	  	  		<div id="list"></div>
		  	</div>
  		</fieldset>
    </div>
	<div style="float:right;margin-top:5px;" id="edit">
		<fieldset style="height:100%;">
			<legend> <b>Editor </legend></b>
			<div id="buttons" style="padding-bottom:5px;text-align:center;width:100%">
				Filename: <font id="file_editing"></font>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				<button onClick="javascript:fileSave();" class=small>Save</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				<button onClick="javascript:fileClose();" class=small>Close</button>
			</div>
			
	  	  	<div id="editor" style="width:100%;" align=left>
				&nbsp;
			</div>
  
  		</fieldset>
	</div>

<BR>
	 
	<div style="width:100%;" id="console">
		<fieldset>
			<legend><b>Console / <button onClick="javascript:closeConsole();" class="small">Close</button></legend></b>
			<textarea id="Console-log" style="height:140px;width:100%;" readonly="ReadOnly"></textarea>
    	 </fieldset>
 	</div>		

</body>






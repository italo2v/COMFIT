<!--
"""This file contains code for use with "Web2CompileCloud",
by Italo C. Brito, Geovane Mattos, Marina Vianna, Claudio C. Miceli available from labnet.nce.ufrj.br

Copyright 2015 - UFRJ
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""
-->
<head>
<script src="static/JS/jquery.js" type="text/javascript" charset=utf-8></script>
<title>COMFIT</title>
<link rel="stylesheet" type="text/css" href="static/css/style.css">
<link rel="stylesheet" type="text/css" href="static/css/jquery-ui.css">
  <script src="static/JS/globals.js" type="text/javascript" charset="utf-8"></script>
  <script src="static/JS/cooja.js" type="text/javascript" charset="utf-8"></script>
  <script src="static/JS/jquery-ui.js" type="text/javascript" charset="utf-8"></script>
  <script src="static/src-min/ace.js" type="text/javascript" charset="utf-8"></script>
</head>
	
<body bgcolor=#E5E5E5>

	<div align="center"> 
		<b><font size=5 color=#2720E9 face=Arial>COMFIT</font> - <button id="openOrion">Open Orion Editor</button></b>
	</div>
	
	<div style="float:left;margin-top:5px;" id="files">
		<fieldset style="height:100%;">
			<legend> <b>Project List</legend></b>
			<div style="overflow-y: scroll;" id="maxsizelist">
	  	  		<div id="list"></div>
		  	</div>
  		</fieldset>
    </div>
	<div style="float:right;margin-top:5px;" id="edit">
		<fieldset style="height:100%;">
			<legend id="legend"> </legend>
			<div id="buttons" style="padding-bottom:5px;text-align:center;width:100%">
				<span id="filePath" style="display:none;"></span>
				<span id="projectName" style="display:none;"></span>
				Filename: <span id="file_editing"></span><span id="changed"></span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				<button onClick="javascript:saveFile();" class=small>Save</button>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
				<button onClick="javascript:closeFile();" class=small>Close</button>
			</div>
			
	  	  	<div id="editor" style="width:100%;" align=left>
				&nbsp;
			</div>
	  	  	<div id="coojaGUI" style="width:100%;" align=left>
				
				<div id="menu">
				  <span>Simulation<ul>
				    <li>Start</li>
				    <li>Configure...</li>
				  </ul>
				  </span>
				  <span>Motes<ul>
				    <li>Add motes...</li>
				    <li>Remove all motes</li>
				  </ul>
				  </span>
				</div>
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






"""This file contains code for use with "Web2CompileCloud",
by Italo C. Brito, Geovane Mattos, Marina Vianna, Claudio C. Miceli available from labnet.nce.ufrj.br

Copyright 2015 - UFRJ
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""


# -*- coding: utf-8 -*-
import os, json
from bottle import *
import signal
import pexpect
import subprocess

tinyos_dir = '/opt/tinyos-2.1.2/apps/Blink/'

def escreve(username,password):

    # insiro quem se cadastrou em um arquivo texto
    arquivo = open("numeros.txt","w")
    arquivo.write("%s" % username+"-"+password+"\n")
    arquivo.close()

	

@route('/')
def inicio():
    return template("tinyos")


'''
@route('/login')
def login():
    return template('formulario')

@route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')

    escreve(username,password)

    if username == "w2c" and password == "labnet":
        redirect('/index')
    else:
        return template('erro_senha', item=username.lower())
	
'''
@route('/tinyos')
def tinyos():
	
	return template("tinyos")
@route('/iotlab')
def iotlab():
	
	return template("iotlab")
	
@get('/static/src-min/:filename')
def ace(filename):
     return static_file(filename, root='static/src-min') 
     
@get('/static/JS/:filename')
def ace(filename):
     return static_file(filename, root='static/JS')
     
@get('/static/css/images/:filename')
def ace(filename):
     return static_file(filename, root='/static/css/images/:filename')

@get('/static/images/:filename')
def img(filename):
     return static_file(filename, root='static/images')

@get('/static/css/:filename')
def css(filename):
     return static_file(filename, root='static/css')

@route('/upload', method='POST')
def do_upload():
	
    upload = request.files.get('upload')
	
    if not os.path.exists(tinyos_dir):
            os.makedirs(tinyos_dir)

    if(os.path.isfile(tinyos_dir+upload.filename)):
        return "EXISTS"
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.py','.c','.nc', '.h'):
        return 'File extension not allowed.'
    file_path = "{path}/{file}".format(path=tinyos_dir, file=upload.filename)

    with open(file_path, 'w') as open_file:
        open_file.write(upload.file.read())


@route('/delete', method="POST")
def deletar():
	filename = request.forms.get('filename')
	arquivo = tinyos_dir+filename
		
	if os.path.isfile(arquivo):
		os.remove(arquivo)
		return "TRUE"
	else:	
		return "FALSE"



@route('/saveFilename', method="POST")
def save():
	filename = request.forms.get('filename')
	content = request.forms.get('content')
	arquivo = tinyos_dir+filename
	file_ = open(arquivo, 'w')
	file_.write(content)
	file_.close()
	return "TRUE"

@route('/readFilename', method="POST")
def readFile():
    filename = request.forms.get('filename')
    arquivo = tinyos_dir+filename
    if os.path.isfile(arquivo):
        arquivo = open(arquivo, 'r')
        content = arquivo.read();
        return content
    else:
        return ""
	
    
@route('/listUploads', method="POST")
def listUploads():
        f=[]
        files = os.listdir(os.path.expanduser(tinyos_dir))
        for file in files:
            if(os.path.isdir(file)==False):
                if(file[0] != '.' and file != 'build' and file != '_TOSSIMmodule.so' and file != 'TOSSIM.py' and file != 'simbuild' and file != 'TOSSIM.pyc' and file != 'app.xml'):
                    f.append(file)
        return json.dumps(f)

@route('/execute', method="POST")
def executeFile():
    file = request.forms.get('filename')
    minutes = request.forms.get('minutes')
    os.system('chmod +x '+tinyos_dir+file)
    split = file.split('.')
    ext = split[len(split)-1]
    cmd = tinyos_dir+file
    ret = ''
    if(ext.lower() == 'py'):
        cmd = 'python '+cmd
        try:
            expect = pexpect.run(cmd, timeout=60*int(minutes))
            #expect.expect('$', timeout=60*minutes)
            ret += str(expect)+'\n'
            if os.path.isfile('log.txt'):
                arquivo = open('log.txt', 'r')
                content = arquivo.read();
                os.system('rm -rf log.txt')
                ret  += content
        except:
            ret += '\n***An error has ocurred during the execution, please note that the maximum time is '+int(minutes)+' minutes!\n'
    else:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        ret += out+err+'\n'
        
    return ret

        
@route('/localexec', method="POST")
def localexec():
    cmd = request.forms.get('cmd')
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    msg = "*** Successfully built micaz TOSSIM library."
    error = "gcc: error:"
    if msg in out:
        return msg
    elif error in err:
        split = err.split(error)
        return error+split.pop()
    return out+err+'\n'




run(host='localhost', port=8080)

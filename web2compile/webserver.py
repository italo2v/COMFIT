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
import pymongo
import random, string
import pycurl
from StringIO import StringIO
import urlparse
import pymongo, gridfs
from beaker.middleware import SessionMiddleware


#configure a prefix route
prefix_route = '/web2compile/'

#Contiki directory
CONTIKI_DIR = '/opt/contiki-2.7'

#Web2Compile Config
server_name = '0.0.0.0'
server_port = 8080

#MongoDB Config
mongo_server = 'localhost'
mongo_port = 27017

#OAuth GitHub Config
client_id = 'your_id'
client_secret = 'your_secret'
redirect_uri = 'http://yourdomain.com:8080/auth/github/callback'


#conecting to database
client = pymongo.MongoClient(mongo_server, mongo_port)
db = client['flight-db']
fs = gridfs.GridFS(db)

#used to return a random word to use as state to authenticate at github
def randomword(length):
   return ''.join(random.choice(string.lowercase) for i in range(length))

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}
app = SessionMiddleware(app(), session_opts)

###<static routes>
@get('/static/src-min/:filename')
def ace(filename):
     return static_file(filename, root='static/src-min')

@get('/static/JS/:filename')
def ace(filename):
     return static_file(filename, root='static/JS')
@get('/static/:filename')
def ace(filename):
     return static_file(filename, root='static')

@get('/static/css/images/:filename')
def ace(filename):
     return static_file(filename, root='static/css/images')

@get('/static/images/:filename')
def img(filename):
     return static_file(filename, root='static/images')

@get('/static/css/:filename')
def css(filename):
     return static_file(filename, root='static/css')
###</static routes>

#verify if you are logged in at github with a token
@route('/')
def inicio():
  s = request.environ.get('beaker.session')
  if request.GET.get('token'):
#    response.set_cookie('access_token', request.GET.get('token'), max_age=60*60*15)
     s['access_token'] = request.GET.get('token')
     s.save()

  if request.GET.get('user') and s.get('access_token'):

	buffer = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'https://api.github.com/user?access_token='+s.get('access_token'))
	c.setopt(c.WRITEFUNCTION, buffer.write)
	c.perform()
	c.close()

	user = json.loads(buffer.getvalue()).get('login')
	if user == request.GET.get('user'):
		return template('index')
	else:
		return "<font color=red>Error: You are not allowed to use that username!</font>"
  elif s.get('access_token'):

	buffer = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, 'https://api.github.com/user?access_token='+s.get('access_token'))
	c.setopt(c.WRITEFUNCTION, buffer.write)
	c.perform()
	c.close()

	user = json.loads(buffer.getvalue()).get('login')
	if user:
  		response.status = 303
  		response.set_header('Location', prefix_route+'?user='+user)

  else:

    response.status = 303
    state = randomword(50)
#    response.set_cookie('state', state, max_age=60*60*15)
    s['state'] = state
    s.save()
    response.set_header('Location', 'https://github.com/login/oauth/authorize?client_id='+client_id+'&scope=gist&redirect='+redirect_uri+'&state='+state);


#route to authenticate at github
@route('/auth/github/callback', method="GET")
def auth():
	code = request.GET.get('code')
	state = request.GET.get('state')
	s = request.environ.get('beaker.session')
	if s.get('state') == state:
		data = {'state': state,
			'code': code,
			'client_id': client_id,
			'client_secret': client_secret,
			'redirect_uri': redirect_uri}
		postfields = urlencode(data)

		buffer = StringIO()
		c = pycurl.Curl()
		c.setopt(c.URL, 'https://github.com/login/oauth/access_token')
		c.setopt(c.POSTFIELDS, postfields)
		c.setopt(c.WRITEFUNCTION, buffer.write)
		c.perform()
		c.close()

		resp = dict(urlparse.parse_qs(buffer.getvalue()))
		if resp.get('access_token'):
			access_token = resp.get('access_token')[0]
			response.status = 303
	    		response.set_header('Location', prefix_route+'?token='+access_token)
		else:
			return "<font color=red>Error when authenticating to GitHub!</font>"
	else:
		state = randomword(50)
		s['state'] = state
		s.save()
		response.status = 303
		response.set_header('Location', 'https://github.com/login/oauth/authorize?client_id='+client_id+'&scope=gist&redirect='+redirect_uri+'&state='+state);

#save the file changes
@route('/saveFile', method="POST")
def saveFile():
	path = request.forms.get('path')
	projectname = request.forms.get('projectname')
	user = request.forms.get('user')
	content = request.forms.get('content')
	name = user+'#'+projectname+'#'+path
	File = fs.get_last_version(name)
	fs.delete(File._id)
	fs.put(content, filename=name)
	return "TRUE"

#return the project list
@route('/listProjects', method="POST")
def listProjects():
	user = request.forms.get('user')
	print "Project List of "+str(user)+":"
	projects = []
	for item in db['projects'].find({"username": user}, {'name':1}):
		print item['name']
		projects.append(item['name'])
	return json.dumps(projects)

#return all the resources of a project
@route('/openProject', method="POST")
def openProject():
	user = request.forms.get('user')
	projectname = request.forms.get('projectname')
	print "Resource List of project "+str(projectname)+" of "+str(user)+":"
	resources = []
	for item in db['resources'].find({"username": user, "projectName": projectname, "deleted": False}, {'path':1, 'type':1}):
		if item['path'] and item['type']:
		  print "Type: "+str(item['type'])+" | Path: "+str(item['path'])
		  if item['path'][0] != '.':
		    resources.append({"path" : item['path'], "type" : item['type']})
	return json.dumps(sorted(resources))

#return a file content
@route('/openFile', method="POST")
def openFile():
	user = request.forms.get('user')
	projectname = request.forms.get('projectname')
	path = request.forms.get('path')
	content = fs.get_last_version(user+'#'+projectname+'#'+path).read()
	return content


#used to run python scripts to simulate using TOSSIM library or to run COOJA simulations
@route('/execute', method="POST")
def executeFile():
    path = request.forms.get('path')
    minutes = request.forms.get('minutes')
    user = request.forms.get('user')
    project = request.forms.get('project')

    for item in db['resources'].find({"username": user, "projectName": project, "deleted": False}, {'path':1, 'type':1}):
      if item['path'] and item['type']:
        if item['type'] == 'file':
          file = 'projects/'+user+'/'+project+'/'+item['path']
          filename = item['path'].split('/')[-1]
          folders = item['path'].replace(filename, '')
          os.system('mkdir -p projects/'+user+'/'+project.replace(" ", "\ ")+'/'+folders.replace(" ", "\ "))
          content = fs.get_last_version(user+'#'+project+'#'+item['path']).read()
          arq = open(file, 'w')
          arq.write(content)
          arq.close()


    filename = path.split('/')[-1]
    folder = path.replace(filename, "")
    ext = path.split('.')[-1].lower()
    ret = ''

    if(ext == 'py'):
        os.system('chmod +x projects/'+user+'/'+project.replace(" ", "\ ")+'/'+path.replace(" ", "\ "))
        cmd = 'python '+filename
        try:
            expect = pexpect.run(cmd, cwd=folder, timeout=60*int(minutes))
            print expect
            ret += str(expect)+'\n'
            if os.path.isfile(folder+'log.txt'):
                arquivo = open(folder+'log.txt', 'r')
                log = arquivo.read();
                ret  += log
	    else:
                ret += '\n***Error: Could not find the log.txt file! Try to compile the application first.'
        except:
            ret += '\n***An error has ocurred during the execution, please note that the maximum time is '+str(minutes)+' minutes!\n'
    elif(ext == 'csc'):
        cmd = 'java -mx512m -jar '+CONTIKI_DIR+'/tools/cooja/dist/cooja.jar -nogui="'+filename+'" -contiki="'+CONTIKI_DIR+'"'
	folder = 'projects/'+user+"/"+project+'/'+folder
        process = subprocess.Popen(cmd, cwd=folder, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if(err != ""):
          ret += err+'\n'
        else:
            if os.path.isfile(folder+'COOJA.testlog'):
                arquivo = open(folder+'COOJA.testlog', 'r')
                log = arquivo.read();
                ret  += log

    return ret

#used to run shell commands like: make micaz sim
@route('/localexec', method="POST")
def localexec():
    cmd = request.forms.get('cmd')
    user = request.forms.get('user')
    project = request.forms.get('project')

    for item in db['resources'].find({"username": user, "projectName": project, "deleted": False}, {'path':1, 'type':1}):
      if item['path'] and item['type']:
        if item['type'] == 'file':
          file = 'projects/'+user+'/'+project+'/'+item['path']
          filename = item['path'].split('/')[-1]
          folders = item['path'].replace(filename, '')
          os.system('mkdir -p projects/'+user+'/'+project+'/'+folders)
          content = fs.get_last_version(user+'#'+project+'#'+item['path']).read()
          arq = open(file, 'w')
          arq.write(content)
          arq.close()


    path = 'projects/'+user+'/'+project
    process = subprocess.Popen(cmd, cwd=path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    msg = "*** Successfully built micaz TOSSIM library."
    error = "gcc: error:"
    if msg in out:
        return msg
    elif error in err:
        split = err.split(error)
        return error+split.pop()
    return out+err+'\n'


#delete a specific file - NotUsed
'''@route('/delete', method="POST")
def deletar():
    path = request.forms.get('path')
    projectname = request.forms.get('projectname')
    username = request.forms.get('username')

    return "TRUE"
'''


#upload a file into GridFS - NotUsed
'''@route('/upload', method='POST')
def do_upload():

    upload = request.files.get('upload')
    folder = request.forms.get('folder')
    projectname = request.forms.get('projectname')
    username = request.forms.get('username')

    if(fs.get_last_version(username+'#'+projectname+'#'+folder+"/"+upload.filename).read() != ""):
        return "EXISTS"
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.py','.c','.nc', '.h'):
        return 'File extension not allowed.'

    fs.put(upload.file, filename=username+"#"+projectname+"#"+folder+"/"+upload.filename)
    return "TRUE"
'''

run(app=app, host=server_name, port=server_port)

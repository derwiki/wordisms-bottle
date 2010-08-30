import json
import time

import bottle
from bottle import route, run
from google.appengine.ext.webapp import util 
from google.appengine.ext import db

from models import Response


bottle.debug(True)

@route('/')
def index():
	try:
		context = dict(time_rendered=time.time(), author='Adam Derewecki')
		resp = Response(**context)
		resp.put()
		context['pageloads'] = Response.all().fetch(50)
		return bottle.template('index', context)

	except Exception, e:
		import traceback
		return traceback.format_exc()

@route('/crash')
def crash():
	raise Exception("Test Crash")

@route('/hello')
def hello():
	return "Hello World!"

util.run_wsgi_app(bottle.default_app())

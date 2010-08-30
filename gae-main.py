import bottle
from bottle import route, run
from google.appengine.ext.webapp import util 
from google.appengine.ext import db

import time
bottle.debug(True)

@route('/')
def index():
	context = dict(time_rendered=time.time())
	try:
		class Response(db.Expando):
			time = db.DateTimeProperty(auto_now_add=True)

		resp = Response(**context)
		resp.put()
	except Exception, e:
		return e

	context['models'] = Response.all()
	context['resp'] = resp.all()
	return str(context)
	return "Byam, son! %(time_rendered)s\n\nmodels: %(models)s(end)" % context

@route('/crash')
def crash():
	raise Exception("Test Crash")

@route('/hello')
def hello():
	return "Hello World!"

util.run_wsgi_app(bottle.default_app())

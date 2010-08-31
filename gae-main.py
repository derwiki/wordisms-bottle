import json
import time
import traceback

import bottle
from bottle import route, run
from google.appengine.ext.webapp import util
from google.appengine.ext import db

from models import Response


bottle.debug(True)

@route('/favicon.ico')
def favicon():
	return None

@route('/:name')
def index(name=None):
	try:
		context = dict(time_rendered=time.time(), author=name)
		resp = Response(**context)
		resp.put()
		context['pageloads'] = Response.all().order('-time_rendered').fetch(50)
		context['headers'] = bottle.request.headers
		return bottle.template('index', context)

	except Exception, e:
		return traceback.format_exc()

@route('/:word/:definition')
def add_word(word, definition):
	try:
		definition = Definition(word=word, definition=definition)
		definition.put()
	except Exception, e:
		return json.dumps(result='failure', reason=traceback.format_exc())

@route('/listwords/:


@route('/crash')
def crash():
	raise Exception("Test Crash")

@route('/hello')
def hello():
	return "Hello World!"

util.run_wsgi_app(bottle.default_app())

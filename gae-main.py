import json
import time
import traceback

import bottle
from bottle import route, run
from google.appengine.ext.webapp import util
from google.appengine.ext import db

from models import Response
import models


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

@route('/add_word/:word/:definition')
def add_word(word, definition):
	try:
		word_definition = dict(word=word, definition=definition)
		definition = models.Definition(**word_definition)
		definition.put()
		return json.dumps(dict(result='success', **word_definition))
	except Exception, e:
		return json.dumps(dict(result='failure', reason=traceback.format_exc(), **word_definition))

@route('/list_words/:wordlist_id')
def list_words(wordlist_id):
	pass


@route('/crash')
def crash():
	raise Exception("Test Crash")

@route('/hello')
def hello():
	return "Hello World!"

util.run_wsgi_app(bottle.default_app())

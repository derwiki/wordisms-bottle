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

@route('/access/:name')
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

@route('/add_word/:wordlist_id/:word/:definition')
def add_word(wordlist_id, word, definition):
	try:
		wordlist_id = int(wordlist_id)
		wordlist = models.Wordlist.get_by_id(wordlist_id)
		word_definition = dict(wordlist_key=wordlist_id, word=word, definition=definition)
		definition = models.Definition(**word_definition)
		definition.put()
		return json.dumps(dict(result='success', id=definition.key().id(),  **word_definition))
	except Exception, e:
		return json.dumps(dict(wordlist_key=wordlist_key, result='failure', reason=traceback.format_exc()))#, **word_definition))

@route('/create_wordlist/:name')
def create_wordlist(name):
	wordlist = models.Wordlist(name=name)
	wordlist.put()
	return dict(name=name, wordlist_key=wordlist.key().id())

@route('/list_wordlists')
def list_wordlists():
	context = dict()
	wordlists = models.Wordlist.all()
	return str([(wordlist.key(), wordlist.name) for wordlist in wordlists])

@route('/enumerate_wordlist/:wordlist_id#[0-9]+#')
def enumerate_wordlist(wordlist_id):
	wordlist = models.Wordlist.get_by_id(int(wordlist_id))
	return wordlist.definition_set
	return definitions
	return wordlist


@route('/crash')
def crash():
	raise Exception("Test Crash")

@route('/hello')
def hello():
	return "Hello World!"

util.run_wsgi_app(bottle.default_app())

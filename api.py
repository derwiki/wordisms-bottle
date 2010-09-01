import json
import time
import traceback

import bottle
from bottle import route, run
from google.appengine.ext.webapp import util
from google.appengine.ext import db

import models


bottle.debug(True)

@route('/favicon.ico')
def favicon():
	return None
	return traceback.format_exc()

API_ROOT = '/api'

@route(API_ROOT + '/add_word/:wordlist_id/:word/:definition')
def add_word(wordlist_id, word, definition):
	try:
		wordlist_id = int(wordlist_id)
		wordlist = models.Wordlist.get_by_id(wordlist_id)
		word_definition = dict(wordlist=wordlist, word=word, definition=definition)
		definition = models.Definition(**word_definition)
		definition.put()
		word_definition.pop('wordlist')
		return json.dumps(dict(result='success', id=definition.key().id(), wordlist_id=wordlist.key().id(), **word_definition))
	except Exception, e:
		return json.dumps(dict(wordlist=wordlist.key().id(), result='failure', reason=traceback.format_exc()))#, **word_definition))

@route(API_ROOT + '/update_definition/:definition_id/:new_definition')
def update_definition(definition_id, new_definition):
	definition_id = int(definition_id)
	definition = models.Definition.get_by_id(definition_id)
	definition.definition = new_definition
	definition.put()
	return dict(word=definition.word, definition=definition.definition)

@route(API_ROOT + '/create_wordlist/:name')
def create_wordlist(name):
	wordlist = models.Wordlist(name=name)
	wordlist.put()
	return dict(name=name, id=wordlist.key().id())

@route(API_ROOT + '/list_wordlists')
def list_wordlists():
	context = dict()
	wordlists = models.Wordlist.all()
	return dict((wordlist.key().id(), dict(name=wordlist.name, entries=len(tuple(wordlist.definition_set)))) for wordlist in wordlists)

@route(API_ROOT + '/enumerate_wordlist/:wordlist_id#[0-9]+#')
def enumerate_wordlist(wordlist_id):
	wordlist = models.Wordlist.get_by_id(int(wordlist_id))
	return dict((definition.word, definition.definition) for definition in wordlist.definition_set)

@route('/crash')
def crash():
	raise Exception("Test Crash")

util.run_wsgi_app(bottle.default_app())

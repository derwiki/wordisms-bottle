import json
import time
import traceback

import bottle
from bottle import route, run
from google.appengine.ext.webapp import util
from google.appengine.ext import db

import models


bottle.debug(True)


@route('/')
def index():
	context = dict(
		wordlists=list_wordlists().items()
	)
	return bottle.template('index', context)

@route('/wordlist/:wordlist_id')
def wordlist(wordlist_id):
	wordlist = models.Wordlist.get_by_id(int(wordlist_id))
	context = dict(
		name=wordlist.name,
		wordlist=enumerate_wordlist(int(wordlist_id)),
	)
	#return str(context)
	return bottle.template('wordlist', context)

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
		return json.dumps(dict(result='success', id=definition.key().id(), wordlist_id=wordlist.key().id(), **word_definition)) + '\n'
	except Exception, e:
		return json.dumps(dict(wordlist=wordlist.key().id(), result='failure', reason=traceback.format_exc()))

@route(API_ROOT + '/remove_word_by_id/:word_id')
def remove_word_by_id(word_id):
	try:
		definition = models.Definition.get_by_id(int(word_id))
		definition.delete()
		return json.dumps(dict(definition_id=definition.key().id(), result='success'))
	except Exception, e:
		return json.dumps(dict(result='failure', reason=traceback.format_exc()))

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
	return [dict(word=definition.word, definition=definition.definition, id=definition.key().id()) for definition in wordlist.definition_set]

from functools import wraps
def debug(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		try:
			res = f(*args, **kwargs)
			return res
		except Exception:
			return json.dumps(dict(result='failure', reason=traceback.format_exc()))
	return wrapper

@route(API_ROOT + '/new_question/:wordlist_id')
@debug
def new_question(wordlist_id):
	wordlist = enumerate_wordlist(wordlist_id)
	kwargs = dict(
		definition=models.Definition.get_by_id(int(wordlist[0]['id'])),
		choice_a=models.Definition.get_by_id(int(wordlist[1]['id'])),
		choice_b=models.Definition.get_by_id(int(wordlist[2]['id'])),
		choice_c=models.Definition.get_by_id(int(wordlist[3]['id'])),
		answer=None,
	)
	question = models.Question(**kwargs)
	question.put()
	return str(question.key().id())

@route(API_ROOT + '/show_question/:question_id')
def show_question(question_id):
	question = models.Question.get_by_id(int(question_id))
	return str(question.choice_a.word)
	return str(question)

@route('/crash')
def crash():
	raise Exception("Test Crash")

util.run_wsgi_app(bottle.default_app())

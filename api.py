from functools import wraps
import json
import random
import time
import traceback

import bottle
from bottle import route, run
from google.appengine.ext.webapp import util
from google.appengine.ext import db

import models

bottle.debug(True)

def debug(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		try:
			res = f(*args, **kwargs)
			return res
		except Exception:
			return json.dumps(dict(result='failure', reason=traceback.format_exc()))
	return wrapper

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
		wordlist=json.loads(enumerate_wordlist(int(wordlist_id))),
	)
	return bottle.template('wordlist', context)

@route('/favicon.ico')
def favicon():
	return None

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
	return json.dumps([dict(word=definition.word, definition=definition.definition, id=definition.key().id()) for definition in wordlist.definition_set])

@route(API_ROOT + '/new_question/:wordlist_id')
def new_question(wordlist_id):
	definitions = json.loads(enumerate_wordlist(wordlist_id))
	if len(definitions) < 4:
		return dict(result='failure', reason='Not enough definitions in this wordlist for a question')

	definition_ids = [int(definition['id']) for definition in definitions]
	random_list_item = lambda l: l[random.randint(0, len(l) - 1)]

	choice_ids = []
	while len(choice_ids) < 4:
		candidate_id = random_list_item(definition_ids)
		if candidate_id in choice_ids:
			continue
		else:
			choice_ids.append(candidate_id)

	load_def_by_id = lambda id: models.Definition.get_by_id(id)
	choices = [load_def_by_id(choice_id) for choice_id in choice_ids]
	definition = random_list_item(choices)

	question_kwargs = dict(
		definition=definition,
		choice_a=choices[0],
		choice_b=choices[1],
		choice_c=choices[2],
		choice_d=choices[3],
	)

	question = models.Question(**question_kwargs)
	question.put()
	return json.dumps(dict(id=question.key().id(), definition=str(definition), result='success'))

@route('/show_question/:question_id')
def show_question(question_id):
	question = models.Question.get_by_id(int(question_id))
	if question is None:
		return 'Invalid question_id: %s' % question_id
	question_str = '''%s:
	a) %s
	b) %s
	c) %s
	d) %s''' % (question.definition.definition, question.choice_a.word, question.choice_b.word, question.choice_c.word, question.choice_d.word)
	return question_str

@route('/crash')
def crash():
	raise Exception("Test Crash")

util.run_wsgi_app(bottle.default_app())

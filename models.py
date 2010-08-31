from google.appengine.ext import db

class Response(db.Expando):
	time = db.DateTimeProperty(auto_now_add=True)
	author = db.StringProperty()

	def __str__(self):
		return "%s, %s" % (self.time, self.author)

class User(db.Expando):
	username = db.StringProperty()
	email = db.StringProperty()

class Wordlist(db.Expando):
	def __str__():
		return "models.Wordlist"
#	def kind():
#		return "models.Wordlist"
	name = db.StringProperty()
	creator = User()

class Definition(db.Expando):
	word = db.StringProperty()
	definition = db.StringProperty()
	wordlist = db.ReferenceProperty(Wordlist)

from google.appengine.ext import db

class User(db.Expando):
	username = db.StringProperty()
	email = db.StringProperty()

class Wordlist(db.Expando):
	def __str__(self):
		return "models.Wordlist"

	__repr__ = __str__

	name = db.StringProperty()
	creator = User()

class Definition(db.Expando):
	word = db.StringProperty()
	definition = db.StringProperty()
	wordlist = db.ReferenceProperty(Wordlist)

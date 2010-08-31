from google.appengine.ext import db

class Response(db.Expando):
	time = db.DateTimeProperty(auto_now_add=True)
	author = db.StringProperty()

	def __str__(self):
		return "%s, %s" % (self.time, self.author)

class Definition(db.Expando):
	wordlist_id = db.IntegerProperty()

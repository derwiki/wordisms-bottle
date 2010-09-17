from google.appengine.ext import db

class User(db.Expando):
	username = db.StringProperty()
	email = db.StringProperty()

class Wordlist(db.Model):
	def __str__(self):
		return "<Wordlist name='%s'>" % self.name

	__repr__ = __str__

	name = db.StringProperty()
	creator = User()

class Definition(db.Model):
	def __str__(self):
		return "<Definition '%s'='%s'>" % (self.word, self.definition)

	__repr__ = __str__

	word = db.StringProperty()
	definition = db.StringProperty()
	wordlist = db.ReferenceProperty(Wordlist)

class Question(db.Model):
	definition = db.ReferenceProperty(reference_class=Definition, collection_name='definition_set')
	choice_a = db.ReferenceProperty(reference_class=Definition, collection_name='choice_a_set')
	choice_b = db.ReferenceProperty(reference_class=Definition, collection_name='choice_b_set')
	choice_c = db.ReferenceProperty(reference_class=Definition, collection_name='choice_c_set')
	choice_d = db.ReferenceProperty(reference_class=Definition, collection_name='choice_d_set')
	answer = db.ReferenceProperty(reference_class=Definition, collection_name='answer_set')

	def __str__(self):
		fields = 'definition,choice_a,choice_b,choice_c,choice_d,answer'.split(',')
		return '; '.join('%s: %s' % (field, getattr(self, field)) for field in fields)

	__repr__ = __str__

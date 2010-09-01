import random
import string
import unittest

import api

def rand_string(length):
	return "".join(string.letters[random.randint(0, len(string.letters) - 1)] for _ in xrange(length))

class TestLogic(unittest.TestCase):
	def test_flow(self):
		wordlist_name = rand_string(50)
		resp = api.create_wordlist(wordlist_name)
		self.assertEqual(wordlist_name, resp['name'])
		wordlist_id = resp['id']

		wordlists = api.list_wordlists()
		print wordlists
		

if __name__ == "__main__":
	unittest.main()

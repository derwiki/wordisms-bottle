'''Basic coverage unittest that interacts with Wordisms over the GAE dev server'''

import random
import simplejson as json
import string
import urllib2
import unittest

def get_json_resp(url, post=None):
	resp = urllib2.urlopen(url)
	raw_resp = resp.readlines()[0]
	return json.loads(raw_resp)

def call_api(api_cmd):
	return get_json_resp('http://localhost:8080/api/%s' % api_cmd)

def rand_string(length):
	return "".join(string.letters[random.randint(0, len(string.letters) - 1)] for _ in xrange(length))

class ApiTest(unittest.TestCase):
	def test_flow(self):
		wordlist_name = rand_string(20)
		word = rand_string(10)
		definition = rand_string(30)
		new_definition = rand_string(27)

		# test that the wordlist can be created
		respjson = call_api('create_wordlist/%s' % wordlist_name)
		self.assertEqual(respjson['name'], wordlist_name)
		wordlist_id = respjson['id']
		wordlist_id_key = str(wordlist_id)

		# test that wordlist shows up in list
		respjson = call_api('list_wordlists')
		self.assertTrue(wordlist_id_key in respjson.keys())
		self.assertEqual(respjson[wordlist_id_key]['name'], wordlist_name)
		self.assertEqual(respjson[wordlist_id_key]['entries'], 0)

		# test adding a word
		respjson = call_api('add_word/%s/%s/%s' % (wordlist_id, word, definition))
		self.assertEqual(respjson['definition'], definition)
		self.assertEqual(respjson['word'], word)
		self.assertEqual(respjson['result'], 'success')
		self.assertEqual(respjson['wordlist_id'], wordlist_id)
		word_id = respjson['id']
		word_id_key = str(word_id)

		# test updating a word's definition
		respjson = call_api('update_definition/%s/%s' % (word_id, new_definition))
		self.assertEqual(respjson['word'], word)
		self.assertNotEqual(respjson['definition'], definition)
		self.assertEqual(respjson['definition'], new_definition)

		# test enumerating a word list
		respjson = call_api('enumerate_wordlist/%s' % (wordlist_id))
		self.assertEqual(respjson[word], new_definition)

if __name__ == '__main__':
	unittest.main()

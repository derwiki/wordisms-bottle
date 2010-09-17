Wordlist: {{name}}

<dl>
% for definition in wordlist:
	<dt>{{definition['word']}} ({{definition['id']}})</dt>
	<dd>{{definition['definition']}}</dd>
% end
</dl>

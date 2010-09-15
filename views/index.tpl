Available wordlists ({{ len(wordlists) }}):<br/>
<ul>
% for wordlist_id, wordlist in wordlists:
	<li><a href="/wordlist/{{ wordlist_id }}">{{wordlist['name']}}</a> ({{ wordlist['entries'] }})</li>
% end
</ul>

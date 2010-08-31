50 most recent accesses<br/>
{{headers.get('Host')}} {{headers.items()}}
% for response in pageloads:
{{ response.time_rendered }}, {{response.author}}<br/>
% end

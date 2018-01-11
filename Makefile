
SHELL := /bin/bash
CREDENTIALS := $(shell cat .credentials)


server: 
	hugo server --bind 192.168.56.101 --baseURL http://192.168.56.101 -v  -D  -t revealjs $(PARAM)



MP3S :=$(shell jinja2filter.py --template='{% for name in data.names %}static/spoken/{{name}}.mp3 {% endfor %}' < data/list.json )

CARDS :=$(shell jinja2filter.py --template='{% for name in data.names %}content/20170109/{{name}}.md {% endfor %}' < data/list.json )


get-data:
	 jsonforge spreadsheet.yml


site:
	hugo -t revealjs

cards: $(CARDS)

mp3s: $(MP3S)

content: cards mp3s

static/spoken/%.mp3: static/items/%.json
	export $(CREDENTIALS) ;\
	cat  <(jq --raw-output .spoken <$<) | ./polly.py --voice=$$(jq --raw-output .voice <$<) >$@

content/20170109/%.md: static/items/%.json
	jinja2filter.py  --templatefile=card.jinja2 <$< >$@

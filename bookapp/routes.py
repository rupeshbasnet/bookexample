from bookapp import app
from flask import render_template
import re
from bs4 import BeautifulSoup

@app.route('/')
def index():
	htl = open('bookapp/static/data/output.html')
	html = htl.read()
	links, sections = parse_htmlbook(html)
	# print (sections)
	title = "Sense and Sensibility by Jane Austen"
	image = '/static/images/title_img.jpg' 
	section = []
	for i in range(len(links)):
		section.append(str(sections[links[i]]['title']))
		# print (section)
	return render_template('home.html', title = title, image = image, section = section, numChapters = len(links), links = links)

@app.route('/<page>')
def section(page):
	htl = open('bookapp/static/data/output.html')
	html = htl.read()
	links, sections = parse_htmlbook(html)
	title = sections[links[int(page)]]['title']
	paragraphs = sections[links[int(page)]]['plist']
	section = []
	for i in range(len(links)):
		section.append(str(sections[links[i]]['title']))
	return render_template('section.html', chapter = title, numChapters = len(links), section = section, paragraphs = paragraphs)

def parse_htmlbook(page):
	links = get_chap_links(page)
	sections = {} 
	for ind in range(len(links)):
		section = {}
		start = links[ind]
		# print(start)
		if ind < len(links)-1:
			end = links[ind+1]
			# print (end)
			patt = ('<a name="' + start +
			'"></a>(?P<sectionbody>.*)<a name="' +
			end + '"></a>' )
			match = re.search(patt,page,re.MULTILINE|re.DOTALL)
			if match == None:
				raise Exception('patt: '+patt+'\n\n')
		else:
			patt = ('<a name="' + start + '"></a>(?P<sectionbody>.*)<pre>')
			match = re.search(patt,page,re.MULTILINE|re.DOTALL)
		if match:
			soup = BeautifulSoup(match.group("sectionbody"), 'html.parser')
			plist = [p.contents[0] for p in soup.find_all('p')]
			section['title']= (soup.find('h2').contents)[0]
			section['plist']= plist
			# print (section)
			sections[start] = section
			# print (sections)
	return links, sections

def get_chap_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [str(link.get('href'))[1:]
		for link in soup.find_all('a') if link.get('href')]
	return links

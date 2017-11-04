import re
from bs4 import BeautifulSoup

def parse_htmlbook(page):
	links = get_chap_links(page)
	sections = {} 
	for ind in range(len(links)):
		section = {}
		start = links[ind]
		print(start)
		if ind < len(links)-1:
			end = links[ind+1]
			print (end)
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
			print (section)
			sections[start] = section
			# print (sections)
	return links, sections

def get_chap_links(page):
	soup = BeautifulSoup(page, 'html.parser')
	links = [str(link.get('href'))[1:]
		for link in soup.find_all('a') if link.get('href')]
	return links


def main():
	htl = open('output.html')
	html = htl.read()
	links, sections = parse_htmlbook(html)
	# print (sections)
	links = get_chap_links(html)
	print (len(links))


if __name__ == "__main__":
	main()
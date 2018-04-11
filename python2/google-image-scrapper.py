# -*- coding: utf-8 -*-

import os
import sys
import json
import urllib2

from bs4 import BeautifulSoup

class	colors:
	RED = '\033[91m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	BLUE = '\033[94m'
	PINK = '\033[95m'
	RESET = '\033[0m'

try:

	def	get_soup(url, header):
		return BeautifulSoup(urllib2.urlopen(urllib2.Request(url, headers = header)), 'html.parser')
	
	NAME = 'IMG'
	TYPE = '.gif'
	DIR = 'pics/'

	query = raw_input(colors.YELLOW + "Google Image search: " + colors.RESET)
	query = query.split()
	query = '+'.join(query)	
	target = "https://www.google.com/search?q=" + query + "&tbm=isch&source=lnt&tbs=itp:animated"
	html_header = { 'User-Agent' : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36" }

	print(colors.PINK + target + colors.RESET) # log stuff, to remove later

	soup = get_soup(target, html_header)

	image_meta = [] # contains the link for large original images & type of image
	for o in soup.find_all('div', { 'class' : 'rg_meta' }):
		img_link, img_type = json.loads(o.text)['ou'], json.loads(o.text)['ity']
		image_meta.append((img_link, img_type))

	print(colors.GREEN + "There are a total of " + str(len(image_meta)) + " images." + colors.RESET) # log stuff, to remove later

	if not os.path.exists(DIR):
		os.mkdir(DIR)
		print(colors.BLUE + "Created '" + DIR + "' directory..." + colors.RESET)

	DIR = os.path.join(DIR, query.split()[0]) # creates sub-directory with formatted query string as the name

	if not os.path.exists(DIR):
		os.mkdir(DIR)
		print(colors.BLUE + "Created '" + DIR + "' directory..." + colors.RESET)

	for i, (img, img_type) in enumerate(image_meta):
		try:
			req = urllib2.Request(img, headers = { 'User-Agent' : html_header })
			raw_img = urllib2.urlopen(req).read()

			counter = len([i for i in os.listdir(DIR) if NAME in i]) + 1
			print(colors.YELLOW + str(counter) + colors.RESET)

			if len(img_type) == 0:
				f = open(os.path.join(DIR, NAME + '_' + str(counter) + TYPE), 'wb')
			else:
				f = open(os.path.join(DIR, NAME + '_' + str(counter) + '.' + img_type), 'wb')
			f.write(raw_img)
			f.close()
		except Exception as error:
			print(colors.RED + "Could not load > " + img + colors.RESET)
			print(colors.PINK + str(error) + colors.RESET)

except (KeyboardInterrupt, SystemExit):
	print(colors.RED + "\nProgram interrupted." + colors.RESET)
	sys.exit(0)

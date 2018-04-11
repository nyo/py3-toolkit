#!/usr/bin/python

import requests
import sys
import re
from datetime import datetime

print('\n\t\t\t' + '-' * 22 + '\n\t\t\t WELCOME TO THIS TOOL \n\t\t\t' + '-' * 22 + '\n')

websitesLST = ['steamcommunity.com', 'instagram.com', 'twitter.com', 'reddit.com']
websitesURL = ['http://steamcommunity.com/id/', 'https://www.instagram.com/', 'https://twitter.com/', 'https://www.reddit.com/user/']
websitesMSG = ['The specified profile could not be found.', 'Page Not Found', 'Sorry, that page does', 'reddit.com: page not found']
okNames = []
t = datetime.now()
i = 0

print("[*] Which website would you like to check usernames availability on?\n")
for website in websitesLST:
	print("\t[%s] %s" % (websitesLST.index(website), website))

print("\n[*] Enter choice...")
while True:
	try:
		choice = int(raw_input("[~] "))
		if choice >= 0 and choice < len(websitesURL):
			break
	except:
		pass

print("\n[*] Enter list name...")
while True:
	try:
		namesList = open(raw_input("[~] "), 'r').read().split('\n')
		break
	except:
		pass
print('')

for name in namesList:
	print("[.] Checking availability of '%s'... %s%% done." % (name, int(i / float(len(namesList) - 1) * 100)))
	i += 1
	try:
		ret = requests.get(websitesURL[choice] + name)
		find = re.search(websitesMSG[choice] , ret.content)
		if find is not None and len(name) > 0:
			okNames.append(name)
			print("[+]\t%s is available!" % name)	
	except (KeyboardInterrupt, SystemExit):
		print("\n[x] Program interrupted...")
		break

print("\n[*] Scanning completed, %d available username(s) found, elapsed time: %s." % (len(okNames), datetime.now() - t))
print("\n[*] RESULT(S):")
for name in okNames:
	print('[-] ' + name)

sys.exit()

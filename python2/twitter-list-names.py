#!/usr/bin/python3

import string
import requests
import sys
import re

twttrList = open("@kXXX.txt", "w+")
lowerLowerCase = ['a', 'c', 'e', 'i', 'm', 'n', 'o', 'r', 's', 'u', 'v', 'w', 'z']

def checkUsername(username):
	""" Prints twitterName for each @username. """
	r = requests.get("https://twitter.com/" + username + "/")
	source = r.text.split('\n')
	for line in source:
		if re.search("data-name=", line):
			s = line.rfind("data-name=") + 10
			e = line.rfind("data-protected=")
			res = "@" + username + ": " + line[s:e]
			twttrList.write(res + "\n")
			print(res)
			break

if __name__ == "__main__":

	if len(sys.argv) != 1:
		sys.exit(1)

	try:
		c = 0
		i = 0
		while i < 10:
			#for x in list(string.ascii_lowercase):
			for x in lowerLowerCase:
				c += 1
				checkUsername('an' + str(i) + str(x))
			i += 1
		#print(c)
	except KeyboardInterrupt:
		sys.exit("\nkeyboard interrupt.")
	except Exception as error:
		sys.exit(str(error))
			

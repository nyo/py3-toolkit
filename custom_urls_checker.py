#!/usr/bin/python3

from time import sleep
import xml.etree.ElementTree as ET
import requests
import sys
import re

# List of the messages, easier to change colors and content from here.
MSG_EXIT_USAGE		= "\033[33m" + "usage: python3 %s <word_list>" + "\033[0m"
MSG_EXIT_INTERRUPT	= "\033[31m" + "\n[!] program has been interrupted." + "\033[0m"
MSG_EXIT_ERROR		= "\033[31m" + "\n[!] %s" + "\033[0m" 
MSG_PRINT_INVALID	= "\033[33m" + "/id/%s " + "\033[1m" + ">>> " + "\033[31m" + "Invalid custom URL..." + "\033[0m"
MSG_PRINT_AVAILABLE	= "\033[33m" + "/id/%s " + "\033[1m" + ">>> " + "\033[1;32m" + "Custom URL available!" + "\033[0m"
MSG_PRINT_IN_USE	= "\033[33m" + "/id/%s " + "\033[1m" + ">>> " + "\033[31m" + "Custom URL in use..." + "\033[0m"
MSG_PRINT_BANNED	= "\033[33m" + "/id/%s " + "\033[1m" + ">>> " + "\033[31m" + "Steam profile banned..." + "\033[0m"
MSG_PROFILE_BANNED	= "The profile you're trying to view has been permanently blocked from participating in the Steam Community."

def checkCustomURL(customURL, search=re.compile(r'[^a-zA-Z0-9-_]').search):
	""" Checks if a custom URL is correctly formatted. """
	return not bool(search(customURL))

def addToList(customURL):
	""" Appends an available URL to a text file. """
	try:
		with open("found.txt", "a") as found:
			found.write(customURL + "\n")
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))

def checkUsernameAv(customURL):
	""" Checks if the specified profile could be found. """
	try:
		r = requests.get("http://steamcommunity.com/id/%s/?xml=1" % customURL)
		if re.search(MSG_PROFILE_BANNED, r.text):
			print(MSG_PRINT_BANNED % customURL)
			return
		root = ET.fromstring(r.text.encode("utf-8"))
		if root[0].tag == "error":
			addToList(customURL)
			print(MSG_PRINT_AVAILABLE % customURL)
		else:
			print(MSG_PRINT_IN_USE % customURL)
	except ET.ParseError as error:
		pass
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))

if __name__ == "__main__":

	if len(sys.argv) != 2:
		sys.exit(MSG_EXIT_USAGE % sys.argv[0])

	try:
		wordList = open(sys.argv[1], "r").read().split("\n")
		for customURL in wordList:
			if len(customURL) > 1: # steam does not accept 1 char custom URLs
				if checkCustomURL(customURL):
					checkUsernameAv(customURL)
				else:
					print(MSG_PRINT_INVALID % customURL)
				sleep(0.1)
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INTERRUPT)
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))

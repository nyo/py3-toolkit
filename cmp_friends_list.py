#!/usr/bin/python3

import xml.etree.ElementTree as ET
import requests
import json
import sys

# List of the messages, easier to change colors and content from here.
MSG_EXIT_USAGE		= "\033[33m" + "usage: python3 %s <old_friends_list> <new_friends_list>" + "\033[0m"
MSG_EXIT_INTERRUPT	= "\033[31m" + "\n[!] program has been interrupted." + "\033[0m"
MSG_EXIT_ERROR		= "\033[31m" + "[!] %s" + "\033[0m"
MSG_EXIT_VALUERROR	= "\033[31m" + "[!] json file is not valid." + "\033[0m"
MSG_EXIT_SAME_FL	= "\033[35m" + "[~] friends lists are the same!" + "\033[0m"
MSG_PRINT_DEL		= "\033[33m" + "[-] %s (%s)" + "\033[0m"
MSG_PRINT_ADD		= "\033[32m" + "[+] %s (%s)" + "\033[0m"

def getSteamName(steamID64):
	""" Returns current steamName for a given steamID64. """
	try:
		r = requests.get("https://steamcommunity.com/profiles/%s/?xml=1" % str(steamID64))
		root = ET.fromstring(r.text.encode("utf-8"))
		return str(root[1].text)
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))

def compareFriendLists(oldOne, newOne):
	""" Compares two friends lists, additions & deletions """
	if oldOne == newOne:
		sys.exit(MSG_EXIT_SAME_FL)
	
	# check for deleted friends
	for i in range(len(oldOne["friendsSteamID64"])):
		ID64 = oldOne["friendsSteamID64"][i]["steamID64"]
		found = 0
		for j in range(len(newOne["friendsSteamID64"])):
			if ID64 == newOne["friendsSteamID64"][j]["steamID64"]:
				found = 1
				break
		if found == 0:
			print(MSG_PRINT_DEL % (ID64, getSteamName(ID64)))
	
	# check for added friends
	for i in range(len(newOne["friendsSteamID64"])):
		ID64 = newOne["friendsSteamID64"][i]["steamID64"]
		found = 0
		for j in range(len(oldOne["friendsSteamID64"])):
			if ID64 == oldOne["friendsSteamID64"][j]["steamID64"]:
				found = 1
				break
		if found == 0:
			print(MSG_PRINT_ADD % (ID64, getSteamName(ID64)))
			
if __name__ == "__main__":
	
	if len(sys.argv) != 3:
		sys.exit(MSG_EXIT_USAGE % sys.argv[0])
	
	try:
		oldFriendList = json.load(open(sys.argv[1], "r"))
		newFriendList = json.load(open(sys.argv[2], "r"))
		compareFriendLists(oldFriendList, newFriendList)
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INTERRUPT)
	except ValueError:
		sys.exit(MSG_EXIT_VALUERROR)
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))

#!/usr/bin/python3

import xml.etree.ElementTree as ET
from steam_get_id_64 import getSteamID64
from datetime import datetime
import requests, json, sys

friendDict = {}
friendList = []

# List of the messages, easier to change colors and content from here.
MSG_EXIT_USAGE      = "\033[33m" + "usage: python3 %s <customURL/steamID32/steamID64>" + "\033[0m"
MSG_EXIT_INTERRUPT  = "\033[31m" + "\n[!] program has been interrupted." + "\033[0m"
MSG_EXIT_ERROR      = "\033[31m" + "[!] %s" + "\033[0m"
MSG_EXIT_PRIVATE    = "\033[31m" + "[x] profile is private." + "\033[0m"
MSG_PRINT_ADD       = "\033[32m" + "[+] added %s to friend list." + "\033[0m"

def makeRequest(steamID64):
    """ Checks if the requested profile is valid, and returns XML. """
    steamURL = "https://steamcommunity.com/"
    try:
        r = requests.get(steamURL + "profiles/%s/?xml=1" % steamID64)
        root = ET.fromstring(r.text.encode("utf-8"))
        if root[4].text == "private":
            sys.exit(MSG_EXIT_PRIVATE)
        else:
            r = requests.get(steamURL + "profiles/%s/friends/?xml=1" % steamID64)
            root = ET.fromstring(r.text.encode("utf-8"))
        return (root)
    except Exception as error:
        sys.exit(MSG_EXIT_ERROR % str(error))

def getFriendList(steamID64):
    """ Appends each steamID64 of a Steam friend list, to a list. """
    xml = makeRequest(steamID64)
    for i in range(len(xml[2])):
        record = { "steamID64" : xml[2][i].text }
        print(MSG_PRINT_ADD % xml[2][i].text)
        friendList.append(record)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit(MSG_EXIT_USAGE % sys.argv[0])

    try:
        t = datetime.now()
        steamID64 = getSteamID64(sys.argv[1])
        getFriendList(steamID64)
        friendDict["friendsSteamID64"] = friendList
        with open(t.strftime("fl-%m-%d-%Y.json"), "w+") as jsonFile:
            json.dump(friendDict, jsonFile)
    except KeyboardInterrupt:
        sys.exit(MSG_EXIT_INTERRUPT)
    except Exception as error:
        sys.exit(MSG_EXIT_ERROR % str(error))

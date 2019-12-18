#!/usr/bin/python3

import requests, steam, re

# List of the messages & URLs, easier to change content from here.
MSG_UNKNOWN_ID	= "The given Steam ID is unknown."
MSG_BANNED_ID	= "The given Steam ID is banned from the community."
MSG_PROF_BANNED	= "The profile you're trying to view has been permanently blocked from participating in the Steam Community."
MSG_NOT_FOUND	= "The specified profile could not be found."

class SteamIDException(Exception):
    """ Handles exceptions for unknown or banned Steam ID. """
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

def checkSteamID(steamID64, user_input):
    """ Checks if the given ID is known and not banned. """
    r = requests.get("https://steamcommunity.com/" + "profiles/%s/?xml=1" % str(steamID64))
    if re.search(MSG_NOT_FOUND, r.text):
        raise SteamIDException(MSG_UNKNOWN_ID)
    if re.search(MSG_PROF_BANNED, r.text):
        raise SteamIDException(MSG_BANNED_ID)

def getSteamID64(user_input):
    """ Returns a steamID64 (as an int) for a given Steam profile. """
    steamID64 = steam.steamid.steam64_from_url("https://steamcommunity.com/" + "id/" + user_input) # customURL case
    if steamID64 is None:
        steamID64 = int(steam.SteamID(user_input)) # steamID32 & steamID64 case
    checkSteamID(steamID64, user_input)
    return steamID64

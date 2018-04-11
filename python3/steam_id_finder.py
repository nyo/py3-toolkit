#!/usr/bin/python3

from get_steam_id_64 import getSteamID64
import steam
import sys

# List of the messages, easier to change colors and content from here.
MSG_EXIT_USAGE		= "\033[33m" + "usage: python3 %s <customURL/steamID32/steamID64>" + "\033[0m"
MSG_EXIT_INTERRUPT	= "\033[31m" + "\n[!] program has been interrupted." + "\033[0m"
MSG_EXIT_ERROR		= "\033[31m" + "[!] %s" + "\033[0m" 

def getProfileDetails(steamID64):
	""" Prints all the details linked to a steamID64. """
	steamInstance = steam.SteamID(steamID64)
	sys.stdout.write("\033[32m")
	print("steam3ID:\t" + steamInstance.as_steam3)
	print("steamID32:\t" + steamInstance.as_steam2)
	print("steamID64:\t" + str(steamInstance.as_64))
	sys.stdout.write("\033[0m")

if __name__ == "__main__":

	if len(sys.argv) != 2:
		sys.exit(MSG_EXIT_USAGE % sys.argv[0])

	try:
		steamID64 = getSteamID64(sys.argv[1])
		getProfileDetails(steamID64)
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INTERRUPT)
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))
	

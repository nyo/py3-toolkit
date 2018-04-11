#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sys
import requests
import datetime
from datetime import datetime
from dateutil.parser import parse

if len(sys.argv) != 2:
	sys.exit("Usage: ./%s <usernames_full_list_name>" % sys.argv[0])

class colors:

	RESET = '\033[0m'
	BD_ON = '\033[1m'
	BD_OFF = '\033[22m'
	RED = '\033[31m'
	GREEN = '\033[32m'
	YELLOW = '\033[33m'
	MAGENTA = '\033[35m'
	CYAN = '\033[36m'

def get_timedate(pattern, page_content):

	parsed_content = []
	current_string = ''
	
	for line in page_content:
		current_string = current_string + line
		if re.search('\n', line):
			parsed_content.append(current_string)
			current_string = ''
	
	for line in parsed_content:
		if re.search(pattern, line):
			return (line[112:131])

def name_is_available(last_log_date):

	curr_time = str(datetime.now())
	last_time = parse(last_log_date)
	curr_time = parse(curr_time)

	diff = last_time - curr_time
	if str(diff)[0] is '-':
		ll = abs(int(diff.total_seconds() / (3600 * 24)))
		if ll > 183: # 183 days, 6 months, 365 days / 2
			return (1)
	return (0)	

def main():

	found = []
	website = "https://osu.ppy.sh/u/"
	usernames = open(sys.argv[1], 'r').read().split('\n')

	log_msg = "<div title=\"Last Active\">"   
	non_existant = "The user you are looking for was not found!"

	for username in usernames:
		if len(username) > 2:
			print("%s[*] Checking availability of %s%s%s...%s" % (colors.CYAN, colors.BD_ON, username, colors.BD_OFF, colors.RESET))
			try:
				ret = requests.get(website + username)
				log_date = re.search(log_msg, ret.content)
				if log_date:
					log_date = get_timedate(log_msg, ret.content)
					if name_is_available(log_date) == 1:
						found.append(username)
						print("%s[+] %s/u/%s%s is probably available!!!%s" % (colors.GREEN, colors.BD_ON, username, colors.BD_OFF, colors.RESET))
				elif re.search(non_existant, ret.content):
						print("%s[+] %s/u/%s%s has not been taken!%s" % (colors.GREEN, colors.BD_ON, username, colors.BD_OFF, colors.RESET))
				else:
					print("%s[-] Can't get last log date.%s" % (colors.YELLOW, colors.RESET))
			except Exception as error:
				print("%s%s[x] Error: %s%s%s" % (colors.RED, colors.BD_ON, error, colors.BD_OFF, colors.RESET))
			except (KeyboardInterrupt, SystemExit):
				print("\n%s%s[x] Program Interrupted...%s%s" % (colors.RED, colors.BD_ON, colors.BD_OFF, colors.RESET))
				sys.exit(1)
	
	print("\n%s%s[@] Program is done searching, here is the (raw) results:%s%s" % (colors.MAGENTA, colors.BD_ON, colors.BD_OFF, colors.RESET))
	for available_username in found:
		print(available_username)

if __name__ == "__main__":

	main()
	sys.exit(0)

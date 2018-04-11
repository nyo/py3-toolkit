#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import sys
import re

if len(sys.argv) != 2:
	sys.exit("Usage: ./%s <list_of_group_urls>" % sys.argv[0])

def find_nth(haystack, needle, n):
	
	start = haystack.find(needle)
	while start >= 0 and n > 1:
		start = haystack.find(needle, start + len(needle))
		n -= 1
	return start

def fill_data(line, data):
	
	if re.search("Join Group", line):
		data[0] = True # Group is public!
	if re.search("grouppage_header_abbrev", line):
		data[1] = line[4:find_nth(line, '\t', 5)] # Get group name. (currently unused)
		data[2] = line[line.find('>')+1:find_nth(line, '<', 2)] # Get group abbreviation.
		data[4] = True # Data found, group does exist!
	if re.search("<span class=\"count \">", line):
		data[3] = line[line.find('>')+1:find_nth(line, '<', 2)] # Get member count. (currently unused)
	return data

def print_data(lstlen, data, url, i):
	
	print("~/%s\t--\t%s\t--\t[ %s ]\t--\t[ %s%% done ]" % \
		(url, data[2], "Public" if data[0] else "Private", int(i / lstlen * 100)))

def main():

	i = 1
	data = [None] * 5 # data [Privacy] [Name] [Abbreviation] [Member Count] [Found?]
	ulist = open(sys.argv[1], 'r').read().split('\n')

	for url in ulist:
		data[0] = False # Check if group is public or not: False if `Group is private`.
		data[4] = False # Check if data was found: False if `Not Found`.
		try:
			r = requests.get("https://steamcommunity.com/groups/" + url)
			if r.status_code == requests.codes.ok:
				page_content = r.text.split('\n')
				for line in page_content:
					data = fill_data(line, data)
				if data[4] and not data[0] and len(url) > 0:
					print_data(float(len(ulist) - 1), data, url, i)
			else:
				print("Error: Status Code.")
		except (KeyboardInterrupt, SystemExit):
			sys.exit("Program Interrupted...")
		i += 1

if __name__ == "__main__":
	main()
	sys.exit()

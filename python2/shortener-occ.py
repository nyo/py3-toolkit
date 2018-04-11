#!/usr/bin/python

import sys
import re

if len(sys.argv) != 3:
	sys.exit("Usage: ./%s <full_list_name> <string_to_delete>" % sys.argv[0])

def main():

	word_list = open(sys.argv[1], 'r').read().split('\n')

	for line in word_list:
		find = re.search(sys.argv[2], line)
		if not find and len(line) > 0:
			print(line)

if __name__ == "__main__":
	main()
	sys.exit()

#!/usr/bin/python

import string
import sys
import re

if len(sys.argv) != 2:
	sys.exit("Usage: ./%s <full_list_name>" % sys.argv[0])

def main():

	allowed_char = string.letters + string.digits
	word_list = open(sys.argv[1], 'r').read().split('\n')

	for line in word_list:
		p = True
		for letter in line:
			find = re.search(letter, allowed_char)
			if not find:
				p = False
		if p and len(line) > 0:
			print(line)

if __name__ == "__main__":
	main()
	sys.exit()

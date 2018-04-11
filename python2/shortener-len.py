#!/usr/bin/python

import sys

if len(sys.argv) != 3:
	sys.exit("Usage: ./%s <full_list_name> <lenght_to_keep>" % sys.argv[0])

def main():

	word_list = open(sys.argv[1], 'r').read().split('\n')

	for line in word_list:
		if len(line) == int(sys.argv[2]):
			print(line)

if __name__ == "__main__":
	main()
	sys.exit()

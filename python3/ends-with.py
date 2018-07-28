#!/usr/bin/python3

import requests, re, sys

MSG_EXIT_USE = "usage: python3 %s <extension>"
MSG_EXIT_INT = "\nkeyboard interrupt"
MSG_EXIT_ERR = "error: %s"
MSG_EXIT_NOT = "no words ending with \"%s\" found in this word list"
MSG_EXIT_BAD = "extension \"%s\" contains invalid characters"

if __name__ == "__main__":

	if len(sys.argv) != 2:
		sys.exit(MSG_EXIT_USE % sys.argv[0])

	try:
		if (re.search("\W", sys.argv[1])):
			sys.exit(MSG_EXIT_BAD % sys.argv[1])
		r = requests.get("https://www.morewords.com/ends-with/" + sys.argv[1])
		for result in r.iter_lines():
			line = str(result)
			if re.search("No words ending with", line):
				sys.exit(MSG_EXIT_NOT % sys.argv[1])
			elif re.search("Some random words", line):
				sys.exit(0)
			elif re.search("<a href=\"/word/", line):
				line = re.sub("(.+)<a href=\"/word/(\w+)/\">", "", line)
				word = re.sub("</a><br />'", "", line)
				print(word)
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INT)
	except Exception as error:
		sys.exit(MSG_EXIT_ERR % str(error))

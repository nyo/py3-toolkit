#!/usr/bin/python3

import requests, re, sys, argparse

MSG_EXIT_INT = "\nkeyboard interrupt"
MSG_EXIT_ERR = "error: %s"
MSG_EXIT_NOT = "no words ending with \"%s\" found in this word list"
MSG_EXIT_BAD = "extension \"%s\" contains invalid characters"

parser = argparse.ArgumentParser(description="program that returns word(s) ending with given extension")
parser.add_argument("extension", help="the characters you want words ending with")
parser.add_argument("--fix", help="fixed length for returned words")
parser.add_argument("--min", help="minimum length for returned words")
parser.add_argument("--max", help="maximum length for returned words")
args = parser.parse_args()

if __name__ == "__main__":
	try:
		if (re.search("\W", args.extension)):
			sys.exit(MSG_EXIT_BAD % args.extension)
		elif args.min > args.max:	
			sys.exit(MSG_EXIT_ERR % "min arg better than max arg...")
		r = requests.get("https://www.morewords.com/ends-with/" + args.extension)
		for result in r.iter_lines():
			line = str(result)
			if re.search("No words ending with", line):
				sys.exit(MSG_EXIT_NOT % args.extension)
			elif re.search("Some random words", line):
				sys.exit()
			elif re.search("<a href=\"/word/", line):
				line = re.sub("(.+)<a href=\"/word/(\w+)/\">", "", line)
				word = re.sub("</a><br />'", "", line)
				if args.fix and len(word) == int(args.fix):
					print(word)
				elif not args.fix:
					if not args.min or args.min and len(word) >= int(args.min):
						if args.max and len(word) > int(args.max):
							continue
						print(word)
		sys.exit()
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INT)
	except Exception as error:
		sys.exit(MSG_EXIT_ERR % str(error))

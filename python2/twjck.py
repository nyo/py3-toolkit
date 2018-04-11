#!/usr/bin/python

import requests
import sys
import re
from datetime import datetime

if len(sys.argv) != 3:
	sys.exit("Usage: ./%s <list_of_accounts> <year>" % sys.argv[0])

def fillfound():
	
	found = []
	msg = sys.argv[2] + "&quot;"
	url = "https://twitter.com/"
	ulist = open(sys.argv[1], 'r').read().split('\n')	

	for uname in ulist:
		print("[.] Checking Availability Of '%s'..." % uname)
		try:
			ret = requests.get(url + uname)
			find = re.search(msg , str(ret.content))
			if find and len(uname) > 0:
				found.append(uname)
				print("[+]\t%s\'s Account Has Been Created In %s!" % (uname, sys.argv[2]))
		except (KeyboardInterrupt, SystemExit):
			print("\n[x] Program Interrupted...")
			break
	
	return found

def main():

	t = datetime.now()

	found = fillfound()
	print("\n[*] Scanning completed, %s account(s) found, elapsed time: %s." % (len(found), datetime.now() - t))
	print("\n[*] RESULT(S):")
	for uname in found:
		print("[-] " + uname)

if __name__ == "__main__":
	main()
	sys.exit()

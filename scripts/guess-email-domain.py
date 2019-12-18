#!/usr/bin/python3

import time, sys, os

MSG_EXIT_USAGE		= "\033[33m" + "usage: python3 %s <domain_with_asterisks>" + "\033[0m"
MSG_EXIT_INTERRUPT	= "\033[31m" + "\n[!] program has been interrupted." + "\033[0m"
MSG_EXIT_ERROR		= "\033[31m" + "[!] %s" + "\033[0m"

def cmpDomains(u_domain, k_domain):
	""" Compares two domains, and tells if they match. """
	if len(u_domain) != len(k_domain):
		return False
	for i in range(len(u_domain)):
		if (u_domain[i] != "*") and (u_domain[i] != k_domain[i]):
			return False
	return True

def guessMail(unknown_domain):
	""" Searchs all the matches in a list of known domains. """
	with open(os.path.dirname(os.path.realpath(__file__)) + "/../wordlists/email-domains.txt", "r") as domains_list:
		for line in domains_list:
			known_domain = line.strip("\n")
			if cmpDomains(unknown_domain, known_domain) is True:
				print("\033[32m>\033[0m", known_domain)
				time.sleep(0.1)

if __name__ == "__main__":

	if len(sys.argv) != 2:
		sys.exit(MSG_EXIT_USAGE % sys.argv[0])

	try:
		guessMail(sys.argv[1])
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INTERRUPT)
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))

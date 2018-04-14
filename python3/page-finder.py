#!/usr/bin/python3

import http.client
import argparse
import socket
import time
import sys

MSG_EXIT_INTERRUPT	= "\033[31m" + "\n[!] program has been interrupted." + "\033[0m"
MSG_EXIT_ERROR		= "\033[31m" + "[!] %s" + "\033[0m"

# args parser
parser = argparse.ArgumentParser()
parser.add_argument("website", help="address of the website to get pages on.")
parser.add_argument("--all", help="display all HTTP responses", action="store_true")
parser.add_argument("--success", help="display successful HTTP responses only", action="store_true")
args = parser.parse_args()

class Colors:
	BOLD = "\033[1m"
	RED	= "\033[31m"
	GREEN = "\033[32m"
	YELLOW = "\033[33m"
	BLUE = "\033[34m"
	EOC = "\033[0m"

def checkPage(site, page):
	""" Checks HTTP status when accessing the given page. """
	target = site + page
	if not args.success:
		print(Colors.BLUE + "[*] Accessing %s..." % target + Colors.EOC)
	try:
		c = http.client.HTTPConnection(site)
		c.request("GET", page)
		s = c.getresponse().status
		if s < 200:
			print(Colors.YELLOW + Colors.BOLD + "[!] 1XX: Informational response" + Colors.EOC)
		elif s < 300:
			if args.success:
				print(Colors.GREEN + Colors.BOLD + "[+] 2XX: Success")
			else:
				input(Colors.GREEN + Colors.BOLD + "[+] 2XX: Success (press enter to continue)" + Colors.EOC)
		elif args.all and s < 400:
			print(Colors.YELLOW + Colors.BOLD + "[!] 3XX: Redirection" + Colors.EOC)
		elif args.all and s < 500:
			print(Colors.YELLOW + Colors.BOLD + "[!] 4XX: Client error" + Colors.EOC)
		elif args.all and s < 600:
			print(Colors.YELLOW + Colors.BOLD + "[!] 5XX: Server error" + Colors.EOC)
		c.close()
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))
	return False

def getRobots(connection):
	""" Tries to get content of /robots.txt. """
	try:
		connection.request("GET", "/robots.txt")
		r = connection.getresponse()
		if r.status < 300:
			print(Colors.GREEN + "[-] Content of file `robots.txt`:" + Colors.EOC)
			print(r.read().decode('utf-8'))
		connection.close()
	except:
		pass

def checkSite(site):
	""" Checks if given address exists or is up online. """
	c = http.client.HTTPConnection(site)
	try:
		c.request("HEAD", '/')
		c.getresponse()
		print(Colors.GREEN + "[~] Connection established, online." + Colors.EOC)
		c.close()
		time.sleep(1)
		getRobots(c)
	except Exception:
		sys.exit(Colors.RED + "[!] Cannot reach website..." + Colors.EOC)

if __name__ == "__main__":
	site = sys.argv[1].replace("http://", "").replace("https://", "").replace("/", "")
	try:
		checkSite(site)
		with open("../wordlists/admin.txt", 'r') as pageslist:
			for page in pageslist:
				checkPage(site, "/" + page.strip('\n'))
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INTERRUPT)
	except Exception as error:
		sys.exit(MSG_EXIT_ERROR % str(error))

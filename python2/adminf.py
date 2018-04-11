#!/usr/bin/python

import sys
import httplib
import socket

class	colors:

	RED = '\033[91m'
	GREEN = '\033[92m'
	BLUE = '\033[94m'
	YELLOW = '\033[93m'
	ENDC = '\033[0m'

class	main():
		
	def	__init__(self):
		self.admin_locate()
		
	def	admin_locate(self):
		try:
			try:
				site = raw_input(colors.BLUE + "Enter the Web Site URL: " + colors.ENDC)
				site = site.replace("http://", "")
				print(colors.YELLOW + "\n\t[+] Connection Established, It's Online.\n" + colors.ENDC)
			except (httplib.HTTPResponse, socket.error) as Exit:
				print(colors.RED + "\t[!] Cannot Connect the Website, It might be offline or invalid URL.\n" + colors.ENDC)
				sys.exit()

			print(colors.YELLOW + "\t[*] Scanning: " + site + colors.ENDC + "\n")

			wordfile = open("../wordlists/admin.txt", "r")
			wordlist = wordfile.readlines()
			wordfile.close()

			for word in wordlist:
				admin = word.strip("\n")
				admin = "/" + admin
				target = site + admin
				print(colors.YELLOW + "[*] Checking: " + target + colors.ENDC)
				connection = httplib.HTTPConnection(site)
				connection.request("GET", admin)
				response = connection.getresponse()

				if response.status == 200:
					print(colors.GREEN + "\n\t+" + (28 + len(target)) * "-" + "+" + colors.ENDC)
					print("%s %s" % (colors.GREEN + "\t    [!] Admin Page Found! " + colors.ENDC, colors.GREEN + target + colors.ENDC))
					print(colors.GREEN + "\t+" + (28 + len(target)) * "-" + "+\n" + colors.ENDC)
					raw_input(colors.YELLOW + "[*] Press enter to continue.\n" + colors.ENDC)
				elif response.status == 301:
					print(colors.RED + "[!] 302 :: Moved Permanently." + colors.ENDC)
				elif response.status == 302:
					print(colors.RED + "[!] 302 :: URL redirection." + colors.ENDC)
				elif response.status == 404:
					print(colors.RED + "[!] 404 :: Error: Not Found." + colors.ENDC)
				elif response.status == 410:
					print(colors.RED + "[!] 410 :: Resource requested is no longer available." + colors.ENDC)
				else:
					print("%s %s" % (colors.RED + "Unknown Response: " + colors.ENDC, colors.RED + str(response.status) + colors.ENDC))
				connection.close()

		except (httplib.HTTPResponse, socket.error):
			print(colors.RED + "\n[!] Session Cancelled, An Error Occured." + colors.ENDC)
			print(colors.RED + "[!] Check Your Internet Connection!" + colors.ENDC)
		except (KeyboardInterrupt, SystemExit):
			print(colors.RED + "\n[!] Session Interrupted and Cancelled" + colors.ENDC)

if __name__ == "__main__":
	main()
	sys.exit()

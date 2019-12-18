#!/usr/bin/python3

import requests
import socket
import sys

MSG_EXIT_USE = "usage: python3 %s <ipv4_address>"
MSG_EXIT_INT = "\nkeyboard interrupt."
MSG_EXIT_ERR = "error: %s"

def isValidAddress(ip_address):
	""" Checks if an IP address is valid or not (thanks to https://stackoverflow.com/a/4017219). """
	try:
		socket.inet_pton(socket.AF_INET, ip_address)
	except AttributeError:
		try:
			socket.inet_aton(ip_address)
		except socket.error:
			return False
		return ip_address.count(".") == 3
	except socket.error:
		return False
	return True

def printDetails(request_json):
	""" Prints details for an IP lookup request. """
	print("[+] lookup information for: %s" % request_json["query"])
	print("[+] geolocation IP informations:")
	print("latitude  > %s" % str(request_json["lat"]))
	print("longitude > %s" % str(request_json["lon"]))
	print("country   > %s [%s]" % (request_json["country"], request_json["countryCode"]))
	print("region    > %s [%s]" % (request_json["regionName"], request_json["region"]))
	print("city      > %s (%s)" % (request_json["city"], request_json["zip"]))
	print("timezone  > %s" % request_json["timezone"])
	print("[+] general IP informations:")
	print("isp               > %s" % request_json["isp"])
	print("as number/name    > %s" % request_json["as"])
	print("organization name > %s" % request_json["org"])
	
def lookupAddress(ip_address):
	""" Gets details about the given IP address. """
	
	api_link = "http://ip-api.com/json/"
	if isValidAddress(ip_address) is False:
		sys.exit(MSG_EXIT_ERR % "invalid ip address.")

	try:
		request = requests.get(api_link + ip_address)
		request_json = request.json()
		if request_json["status"] == "success":
			printDetails(request_json)
		else:
			sys.exit(MSG_EXIT_ERR % str(request.status_code))
	except requests.exceptions.RequestException as error:
		sys.exit(MSG_EXIT_ERR % str(error))

if __name__ == "__main__":

	if len(sys.argv) != 2:
		sys.exit(MSG_EXIT_USE % sys.argv[0])

	try:
		lookupAddress(sys.argv[1])
	except KeyboardInterrupt:
		sys.exit(MSG_EXIT_INT)
	except Exception as error:
		sys.exit(MSG_EXIT_ERR % str(error))

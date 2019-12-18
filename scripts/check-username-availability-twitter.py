#!/usr/bin/python3

# if you wanna automatically check for username availability every 30 seconds
# crontab -e
# * * * * * /usr/bin/python3 /root/twitter/check-twitter-username.py --username "admin" 2>&1 >/path/to/logs
# * * * * * ( sleep 30 ; /usr/bin/python3 /root/twitter/check-twitter-username.py --username "admin" 2>&1 >/path/to/logs )

import requests, sys, re, argparse, time
from datetime import datetime

TXT_FREE_USERNAME = "\<title\>Twitter \/ \?\<\/title\>"
TXT_SUSPENDED = "\<title\>Twitter \/ Compte Suspendu<\/title>"

parser = argparse.ArgumentParser()
parser.add_argument("--username", help="the username to check availability for")
parser.add_argument("--wordlist", help="a list of usernames to check availability for")
args = parser.parse_args()

class Twitter():

    def __init__(self):
        self.BASE_URL = "https://twitter.com"

    def is_available(self, handle):
        date = str(datetime.now())
        r = requests.get("%s/%s" % (self.BASE_URL, handle))
        html = r.text.encode("utf-8").decode("ISO-8859-1")
        if re.search(TXT_FREE_USERNAME, html):
            print("[%s] the username '%s' is free!" % (date, handle))
        elif re.search(TXT_SUSPENDED, html):
            print("[%s] the username '%s' has been suspended..." % (date, handle))
        else:
            print("[%s] the username '%s' is in use." % (date, handle))

if __name__ == "__main__":

    if not args.username and not args.wordlist:
        sys.exit(parser.print_help())

    try:
        app = Twitter()
        if args.username:
            handle = str(args.username)
            app.is_available(handle)
        else:
            with open(args.wordlist) as wordlist:
                for word in wordlist:
                    handle = word.strip()
                    app.is_available(handle)
                    time.sleep(2)
        sys.exit()
    except KeyboardInterrupt:
        sys.exit("\nkeyboard interrupt")
    except Exception as error:
        sys.exit("error: %s" % str(error))

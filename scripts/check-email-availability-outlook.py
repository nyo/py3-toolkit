#!/usr/bin/python3

import requests, re, json, sys, argparse

# you must give this script strings of the entire address as input, example:
# python3 outlook.py --username "test@outlook.com"
# (it pretty much can check every domain available for registration on outlook.com rn)
#	@nyo -- github.com/nyo

parser = argparse.ArgumentParser()
parser.add_argument("--wordlist", required="--domain" in sys.argv, help="a list of words to check availability for")
parser.add_argument("--domain", required="--wordlist" in sys.argv, help="the domain to check each word availability on")
parser.add_argument("--username", help="a username to check availability for")
parser.add_argument("--pretty", help="prettier output (easier to read when used with wordlist)", action="store_true")
parser.add_argument("--silent", help="disable session messages", action="store_true")
args = parser.parse_args()

class Outlook():

    def __init__(self):
        self.session = requests.Session()
        self.i = 0
        self.uaid = None
        self.uiflvr = None
        self.scid = None
        self.hpgid = None
        self.tcxt = None
        self.apiCanary = None
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            "Host": "signup.live.com",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest"
        }

    def rev_bytes(self, data):
        to_byte = str.encode(data).decode("unicode_escape").encode("ascii")
        to_string = to_byte.decode("unicode_escape").encode("ascii").decode("ascii")
        return to_string

    def start_session(self):
        url = "https://signup.live.com/signup.aspx?lic=1"
        r = self.session.get(url, headers=self.headers)
        self.uaid = re.search("uaid\":\"(.+?)\",", str(r.content)).group(1)
        self.uiflvr = int(re.search("uiflvr\":(.+?),", str(r.content)).group(1))
        self.scid = int(re.search("scid\":(.+?),", str(r.content)).group(1))
        self.hpgid = int(re.search("hpgid\":(.+?),", str(r.content)).group(1))
        self.tcxt = self.rev_bytes(re.search("tcxt\":\"(.+?)\"},", str(r.content)).group(1))
        self.apiCanary = self.rev_bytes(re.search("apiCanary\":\"(.+?)\",", str(r.content)).group(1))
        if not args.silent:
            print("got outlook session")	
	
    def is_available(self, word):
        if self.i >= 10:
            if not args.silent:
                print("starting new session...")
            self.i = 0
            self = Outlook()
            self.start_session()
        self.i += 1
        url = "https://signup.live.com/API/CheckAvailableSigninNames?uaid={}&lic=1".format(self.uaid)
        data = {
            "signInName": word,
            "performDisambigCheck": True,
            "includeSuggestions": True,
            "uaid": self.uaid,
            "uiflvr": self.uiflvr,
            "scid": self.scid,
            "hpgid": self.hpgid,
            "tcxt": self.tcxt
        }
        self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=utf-8"
        self.headers["canary"] = self.apiCanary
        r = self.session.post(url, headers=self.headers, data=json.dumps(data))
        # print(self.session.cookies)
        # print(json.dumps(data, indent=4))
        # print(json.dumps(self.headers, indent=4))
        return r.json()

if __name__ == "__main__":

    if not args.username and not args.wordlist:
        sys.exit(parser.print_help())
	
    try:
        app = Outlook()
        app.start_session()
        if args.username:
            ret = app.is_available(args.username)
            print(json.dumps(ret, indent=4))
        else:
            with open(args.wordlist) as wordlist:
                for word in wordlist:
                    word = word.strip() if not args.domain else word.strip() + "@" + args.domain
                    ret = app.is_available(word)
                    if args.pretty:
                        if "error" not in ret:
                            print("%s [ %s ]" % ("OK" if ret["isAvailable"] == True else "--", word))
                    else:
                        print(json.dumps(ret, indent=4))
            sys.exit()
    except KeyboardInterrupt:
        sys.exit("\nkeyboard interrupt")	
    except Exception as error:
        sys.exit("error: %s" % error)

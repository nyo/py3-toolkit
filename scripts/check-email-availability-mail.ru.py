#!/usr/bin/python3

import requests, json, sys, argparse, time, psutil, os, signal
from urllib.parse import quote

parser = argparse.ArgumentParser()
parser.add_argument("--wordlist", required="--domain" in sys.argv, help="a list of words to check availability for")
parser.add_argument("--domain", required="--wordlist" in sys.argv, help="the domain to check each word availability on")
parser.add_argument("--username", help="a username to check availability for")
parser.add_argument("--pretty", help="prettier output (easier to read when used with wordlist)", action="store_true")
parser.add_argument("--silent", help="disable session messages", action="store_true")
args = parser.parse_args()

class MailRu():
    
    def __init__(self):
        self.proxies = {
            "http": "socks5://localhost:9050",
            "https": "socks5://localhost:9050"
        }
        self.session = requests.Session()
        self.i = 0
        self.body = "email=%s" + "&name={\"first\":\"\",\"last\":\"\"}                                                              \
                    &birthday={\"day\":\"\",\"month\":\"\",\"year\":\"\"}                                                           \
                    &htmlencoded=false" + "&utm={\"source\":\"\",\"medium\":\"\",\"campaign\":\"\",\"term\":\"\",\"content\":\"\"}  \
                    &referrer=https://mail.ru/?from=inbox.ru"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
            "Host": "account.mail.ru",
            "Connection": "keep-alive",
            "X-Requested-With": "XMLHttpRequest"
        }

    def send_hup(self):
        if not args.silent:
            print("getting new proxy...")
        try:
            for proc in psutil.process_iter():
                if proc.as_dict()["name"] == "tor":
                    pid = proc.as_dict()["pid"]
                    os.kill(pid, signal.SIGHUP)
            time.sleep(1.5)
            if not args.silent:
                print("new proxy: %s" % requests.get("https://api.ipify.org?format=json", proxies=self.proxies).json()["ip"])
        except Exception as error:
            sys.exit("error: %s" % str(error))

    def start_session(self):
        if not args.silent:
            print("starting new session...")
        self.send_hup()
        url = "https://account.mail.ru/signup"
        r = self.session.get(url, headers=self.headers, proxies=self.proxies)
        if not args.silent:
            print("got mail.ru session")

    def is_available(self, word):
        if self.i >= 10:
            #sys.exit()
            self.i = 0
            self = MailRu()
            self.start_session()
        self.i += 1
        url = "https://account.mail.ru/api/v1/user/exists"
        data = quote(self.body % (word if not args.domain else word + "@" + args.domain), safe="/=&")
        self.headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        r = self.session.post(url, headers=self.headers, data=data, proxies=self.proxies)
        return r.json()

if __name__ == "__main__":

    if not args.username and not args.wordlist:
        sys.exit(parser.print_help())

    try:
        app = MailRu()
        app.start_session()
        if args.username:
            ret = app.is_available(args.username)
            print(json.dumps(ret, indent=4))
        else:
            wordlist = open(args.wordlist, "r")
            for word in wordlist:
                for attempt in range(3):
                    try:
                        ret = app.is_available(word.strip())	
                        if args.pretty and ret["status"] == 200:
                            print("%s [ %s ]" % ("\x1b[31m--\x1b[0m" if ret["body"]["exists"] == True else "\x1b[32mOK\x1b[0m", ret["email"]))
                        else:
                            print(json.dumps(ret, indent=4))
                    except requests.exceptions.ConnectionError:
                        continue
                    break
        sys.exit()
    except KeyboardInterrupt:
        sys.exit("\nkeyboard interrupt")	
    except Exception as error:
        sys.exit("error: %s" % str(error))

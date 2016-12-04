# coding:utf-8
import tweepy
import time
import json
import re

def brainfuck(code):
    Str = ""
    arrayNumber = 0
    p = 0
    inputInt = [0]
    code = code.encode("utf-8")
    while arrayNumber < len(code):
        print str(arrayNumber) + "<" + str(len(code)) + ":" + code[arrayNumber]
        if p >= len(inputInt):
            inputInt.append(0)
        if code[arrayNumber] == ">":
            p += 1
        elif code[arrayNumber] == "<":
            p -= 1
        elif code[arrayNumber] == "+":
            inputInt[p] += 1
        elif code[arrayNumber] == "-":
            inputInt[p] -= 1
        elif code[arrayNumber] == ".":
            Str += chr(inputInt[p])
        elif code[arrayNumber] == ",":
            inputInt[p] = ord(raw_input()[0])
        elif code[arrayNumber] == "]":
            if inputInt[p] > 0:
                while code[arrayNumber] != "[":
                    arrayNumber -= 1
        else:
            if code[arrayNumber] != "[":
                print "Error:" + code[arrayNumber]
                return None
        arrayNumber += 1
    return Str

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            print "Name:" + status.user.name
            print "@" + status.user.screen_name
            print status.text
            print "ID:" + str(status.id) + "\n"

            pattern = "#brain"
            if re.search(pattern, status.text) is not None:
                stre = re.sub(pattern, "", status.text)
                stre = re.sub("&gt;", ">", stre)
                stre = re.sub("&lt;", "<", stre)
                stre = re.sub("&amp;", "&", stre)
                stre = re.sub("\n", "", stre)
                stre = stre.strip()
                stre = stre.encode("utf-8")
                print stre
                print len(stre)
                brainStr = brainfuck(stre)
                if brainStr is not None:
                    api.update_status("@" + status.user.screen_name + " " + brainStr, status.id)
            else:
                print "not brainfuck"
            
        except:
            import traceback
            traceback.print_exc()

    def on_error(self, status_code):
        if status_code == 420:
            print str(status_code)
            return False

def oauth():
    CK = "vnFmObEfM2UrG0gD84936ugN0"
    CS = "8nh3iu5Xbwa9JnUlrluCdeAOtsxYA9kpxI7L97oN3rOcJIgLor"
    AT = "750966877325787136-32b3fydkQN6k08vxA1aernKagIMD4pJ"
    AS = "AjHmSpzuvTW2H5DxggjcAHy2G98RpkibF6ryhY1ZEsAhE" 

    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    return auth

api = tweepy.API(oauth())
stream = tweepy.Stream(auth=api.auth, listener=StreamListener())

while True:
    try:
        stream.userstream()
    except:
        print "E:"
        time.sleep(30)
        stream = tweepy.Stream(auth=api.auth, listener=StreamListener())
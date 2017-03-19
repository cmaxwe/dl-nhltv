import json
import cookielib
from datetime import datetime
import os
import subprocess
from Carbon.Aliases import false

MASTER_FILE_TYPE = 'master_tablet60.m3u8'
SETTINGS_FILE = 'settings.json'
COOKIES_LWP_FILE = "cookies.lwp"
COOKIES_TXT_FILE = "cookies.txt"

# User Agents
UA_GCL = 'NHL1415/5.0925 CFNetwork/711.4.6 Darwin/14.0.0'
UA_IPHONE = 'Mozilla/5.0 (iPhone; CPU iPhone OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143 iphone nhl 5.0925'
UA_IPAD = 'Mozilla/5.0 (iPad; CPU OS 8_4 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Mobile/12H143 ipad nhl 5.0925'
UA_NHL = 'NHL/2542 CFNetwork/758.2.8 Darwin/15.0.0'
UA_PC = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
UA_PS4 = 'PS4Application libhttp/1.000 (PS4) libhttp/3.15 (PlayStation 4)'


def tprint(outString):
    outString = datetime.now().strftime('%m/%d/%y %H:%M:%S - ') + outString
    print(outString)


def find(source, start_str, end_str):
    start = source.find(start_str)
    end = source.find(end_str, start + len(start_str))

    if start != -1:
        return source[start + len(start_str):end]
    return ''


def getSetting(sid):
    # Ensure file exists
    if not os.path.isfile(SETTINGS_FILE):
        createSettingsFile(SETTINGS_FILE)

    # Load the settings file
    with open(SETTINGS_FILE, "r") as settingsFile:
        j = json.load(settingsFile)
    settingsFile.close()
    if sid in j:
        return(j[sid])
    return('')


def setSetting(sid, value):
    # Ensure file exists
    if not os.path.isfile(SETTINGS_FILE):
        createSettingsFile(SETTINGS_FILE)

    # Write to settings file
    with open(SETTINGS_FILE, "r") as settingsFile:
        j = json.load(settingsFile)

    settingsFile.close()
    j[sid] = value

    with open(SETTINGS_FILE, "w") as settingsFile:
        json.dump(j, settingsFile, indent=4)

    settingsFile.close()


def saveCookiesAsText():
    cjT = cookielib.MozillaCookieJar(COOKIES_TXT_FILE)

    cj = cookielib.LWPCookieJar(COOKIES_LWP_FILE)
    cj.load(COOKIES_LWP_FILE, ignore_discard=False)
    for cookie in cj:
        cjT.set_cookie(cookie)
    cjT.save(ignore_discard=False)


def touch(fname):
    with open(fname, 'w'):
        pass


def createSettingsFile(fname):
    with open(fname, "w") as settingsFile:
        jstring = """{
    "session_key": "000",
    "media_auth": "mediaAuth=000",
    "lastGameID": 2015030166
}"""
        j = json.loads(jstring)
        json.dump(j, settingsFile, indent=4)


def createMandatoryFiles():
    # TODO: Move into each individual module:
    if not os.path.isfile(COOKIES_LWP_FILE):
        touch(COOKIES_LWP_FILE)

    if not os.path.isfile(COOKIES_TXT_FILE):
        touch(COOKIES_TXT_FILE)


def which(program):
    command = 'which ' + program
    returnCode = subprocess.Popen(command, shell=True).wait()
    if returnCode == 0:
            return True
    return False

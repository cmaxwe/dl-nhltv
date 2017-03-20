from nhltv_lib.silenceskip import silenceSkip
from nhltv_lib.download_nhl import DownloadNHL
from nhltv_lib.common import tprint, saveCookiesAsText, getSetting, which
from nhltv_lib.common import setSetting, createMandatoryFiles
import argparse
from nhltv_lib.video import reEncode
from nhltv_lib.teams import Teams
import time
MOBILE_VIDEO = False
RETRY_ERRORED_DOWNLOADS = False
DOWNLOAD_FOLDER = ""
TEAMID = 0
dl = DownloadNHL()


def main():
    """
     Find the gameID or wait until one is ready
    """

    createMandatoryFiles()
    gameID = None
    while True:
        gameID, contentID, eventID = dl.getGameId()
        if gameID is not None:
            break
        # If there is no game in the file wait a day
        tprint("No game in latest json. Waiting a day.")
        waitTime = 86400
        time.sleep(waitTime)

    # When one is found then fetch the stream and save the cookies for it
    tprint('Fetching the stream URL')
    stream_url, _, game_info = dl.fetchStream(gameID, contentID, eventID)
    saveCookiesAsText()

    # Wait 15 minutes for it to propagate
    # waitTime = 60 * 20
    # tprint("Game ready! Waiting for " + str(waitTime/60) + ' minutes for it to finish propagating.')
    # time.sleep(waitTime)

    tprint("Downloading stream_url")
    outputFile = str(gameID) + '_raw.mkv'
    dl.download_nhl(stream_url, outputFile)

    # Update the settings to reflect that the game was downloaded
    setSetting('lastGameID', gameID)

    # Remove silence
    tprint("Removing silence...")
    newFileName = DOWNLOAD_FOLDER + game_info + "_" + str(gameID) + '.mkv'
    silenceSkip(outputFile, newFileName)

    if MOBILE_VIDEO is True:
        tprint("Re-encoding for phone...")
        reEncode(newFileName, str(gameID) + '_phone.mkv')


def parse_args():

    global DOWNLOAD_FOLDER
    global RETRY_ERRORED_DOWNLOADS
    global MOBILE_VIDEO

    if which("ffmpeg") is False:
        print ("Missing ffmpeg command please install or check PATH exiting...")
        exit(1)

    if which("aria2c") is False:
        print ("Missing aria2c command please install or check PATH exiting...")
        exit(1)

    parser = argparse.ArgumentParser(description='%(prog)s: Download NHL TV')

    parser.add_argument(
        "-t", "--team",
        dest="TEAMID",
        help="Team ID i.e. 17 or DET or Detroit",
        required=True)

    parser.add_argument(
        "-u", "--username",
        dest="USERNAME",
        help="User name of your NHLTV account")

    parser.add_argument(
        "-p", "--password",
        dest="PASSWORD",
        help="Password of your NHL TV account ")

    parser.add_argument(
        "-q", "--quality",
        dest="QUALITY",
        help="is highest by default you can set it to 5000, 3500, 1500, 900")

    parser.add_argument(
        "-d", "--download_folder",
        dest="DOWNLOAD_FOLDER",
        help="Output folder where you want to store your final file like $HOME/Desktop/NHL/")

    parser.set_defaults(feature=True)
    parser.add_argument(
        "-r", "--retry",
        dest="RETRY_ERRORED_DOWNLOADS",
        action='store_true',
        help="Usually works fine without, Use this flag if you want it perfect")

    parser.add_argument(
        "-m", "--mobile_video",
        dest="MOBILE_VIDEO",
        action='store_true',
        help="Set this to also encode video for mobile devices")

    args = parser.parse_args()

    if args.TEAMID:
        teams = Teams()
        team = teams.getTeam(args.TEAMID)
        dl.teamID = team.id

    if args.USERNAME:
        dl.userName = args.USERNAME
        setSetting("USERNAME", args.USERNAME)
    else:
        dl.userName = getSetting("USERNAME")
    if dl.userName == "":
        print("Missing username, please provide username with -u")
        exit(1)

    if args.PASSWORD:
        dl.passWord = args.PASSWORD
        setSetting("PASSWORD", args.PASSWORD)
    else:
        dl.passWord = getSetting("PASSWORD")
    if dl.passWord == "":
        print("Missing password, please provide password with -p")
        exit(1)

    if args.QUALITY:
        dl.quality = str(args.QUALITY)
    if args.DOWNLOAD_FOLDER:
        DOWNLOAD_FOLDER = args.DOWNLOAD_FOLDER
        setSetting("DOWNLOAD_FOLDER", DOWNLOAD_FOLDER)
    else:
        DOWNLOAD_FOLDER = getSetting("DOWNLOAD_FOLDER")

    if args.RETRY_ERRORED_DOWNLOADS:
        RETRY_ERRORED_DOWNLOADS = args.RETRY_ERRORED_DOWNLOADS
    if args.MOBILE_VIDEO:
        MOBILE_VIDEO = args.MOBILE_VIDEO

    print "parse_args: DOWNLOAD_FOLDER = " + DOWNLOAD_FOLDER
    while(True):
        main()

if __name__ == '__main__':
    parse_args()

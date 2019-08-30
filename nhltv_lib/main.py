from nhltv_lib.download_nhl import DownloadNHL
from nhltv_lib.common import tprint, getSetting, which, wait, saveCookiesAsText
from nhltv_lib.common import setSetting, createMandatoryFiles
import argparse, os, time, glob
from nhltv_lib.teams import Teams
from nhltv_lib.silenceskip import silenceSkip
from nhltv_lib.video import reEncode
MOBILE_VIDEO = False
RETRY_ERRORED_DOWNLOADS = False
DOWNLOAD_FOLDER = ""
RETENTIONDAYS = ""
TEAMID = 0
TEAMIDS = []
CHECKINTERVAL=4
dl = DownloadNHL()

__author__ = "Clayton Maxwell && Helge Wehder && loopway"


def main():
    """
    Find the gameID or wait until one is ready
    """

    while True:

        for TEAMID in TEAMIDS:
            dl.teamID = TEAMID.id

            createMandatoryFiles()
            gameID = None
            waitTimeInMin = 60
            try:
                gameID, contentID, eventID, waitTimeInMin = dl.getGameId()
            except dl.NoGameFound:
                tprint('No new game.')
                continue
            
            except dl.GameStartedButNotAvailableYet:
                tprint('Game has started but is not available yet.')
                continue

            if waitTimeInMin > 0:
                tprint('Game has not started yet.')
                continue

            if gameID is None:
                tprint('Did not find a gameID.')
                continue

            # When one is found then fetch the stream and save the cookies for it
            tprint('Fetching the stream URL')
            while True:
                try:
                    stream_url, _, game_info = dl.fetchStream(gameID, contentID, eventID)
                    break
                except dl.BlackoutRestriction:
                    wait(reason="Game is effected by NHL Game Center blackout restrictions.", minutes=12 * 60)

            saveCookiesAsText()

            tprint("Downloading stream_url")
            outputFile = str(gameID) + '_raw.mkv'
            dl.download_nhl(stream_url, outputFile)

            # Update the settings to reflect that the game was downloaded
            setSetting('lastGameID', gameID, TEAMID.id)

            # Remove silence
            tprint("Removing silence...")
            newFileName = DOWNLOAD_FOLDER + '/' + str(TEAMID.abbreviation) + "_" + game_info + "_" + str(gameID) + '.mkv'
            silenceSkip(outputFile, newFileName)

            if MOBILE_VIDEO is True:
                tprint("Re-encoding for phone...")
                reEncode(newFileName, str(gameID) + '_phone.mkv')

        if RETENTIONDAYS:
            tprint("Running housekeeping ...")
            pathpattern = (DOWNLOAD_FOLDER + "/*.mkv", "*.mkv_download.log")
            now=time.time()
            for pp in pathpattern:
                for f in glob.glob(pp):
                    if os.stat(f).st_mtime < now - RETENTIONDAYS * 86400:
                        tprint("deleting " + f + "...")
                        os.remove(f)


        wait(reason="Checking for new games again in " + str(CHECKINTERVAL) + "hours ...", minutes=CHECKINTERVAL * 60)

def parse_args():

    global DOWNLOAD_FOLDER
    global RETENTIONDAYS
    global CHECKINTERVAL
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
        "--append-action", action="append",
        dest="TEAMID",
        help="Team ID i.e. 17 or DET or Detroit, can be used multiple times",
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
       
    parser.add_argument(
        "-i", "--checkinterval",
        dest="CHECKINTERVAL",
        help="Specify checkinterval in hours to look for new games, default is 4")

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
    
    parser.add_argument(
        "-k", "--keep",
        dest="RETENTIONDAYS",
        help="Specify how many days video and download logs are kept, default is forever")

    args = parser.parse_args()

    if args.TEAMID:
      for TEAMID in args.TEAMID:
        teams = Teams()
        team = teams.getTeam(TEAMID)
        TEAMIDS.append(team)

    if args.USERNAME:
        dl.userName = args.USERNAME
        setSetting("USERNAME", args.USERNAME, 'GLOBAL')
    else:
        dl.userName = getSetting("USERNAME", 'GLOBAL')

    if args.PASSWORD:
        dl.passWord = args.PASSWORD
        setSetting("PASSWORD", args.PASSWORD, 'GLOBAL')
    else:
        dl.passWord = getSetting("PASSWORD", 'GLOBAL')

    if args.QUALITY:
        dl.quality = str(args.QUALITY)
    if args.DOWNLOAD_FOLDER:
        DOWNLOAD_FOLDER = args.DOWNLOAD_FOLDER
        setSetting("DOWNLOAD_FOLDER", DOWNLOAD_FOLDER, 'GLOBAL')
    else:
        DOWNLOAD_FOLDER = getSetting("DOWNLOAD_FOLDER", 'GLOBAL')
        tprint("DOWNLOAD_FOLDER got set to " + DOWNLOAD_FOLDER)

    if args.CHECKINTERVAL:
        CHECKINTERVAL = int(args.CHECKINTERVAL)

    if args.RETRY_ERRORED_DOWNLOADS:
        RETRY_ERRORED_DOWNLOADS = args.RETRY_ERRORED_DOWNLOADS
    if args.MOBILE_VIDEO:
        MOBILE_VIDEO = args.MOBILE_VIDEO

    if args.RETENTIONDAYS:
        RETENTIONDAYS = int(args.RETENTIONDAYS)

    while(True):
        main()


if __name__ == '__main__':
    parse_args()

# dl-nhltv
Download NHL.tv Streams up to 720p60 and remove the commercial breaks

## Requirements:
* *You need A offical NHL.tv account to run this script! This is not for free!*
* Mac or Linux. Sorry Windows users! You could maybe run it through Cygwin?
* python 2.7, aia2c, openssl, ffmpeg

## Steps to get it working once installed...

1. Set your username in the globals.py file
2. Set your password in the globals.py file
3. Set the team id in the globals.py
4. Set your quality in the globals.py file (or leave it at 5000k)

If for step 3 you don't know your team id then load the nhl.tv json and find it in there...
URL for the json: 
http://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.linescore,schedule.scoringplays,schedule.game.content.media.epg&startDate=2016-02-10&endDate=2016-04-10&site=en_nhl&platform=playstation


## Usage:
```
python2.7 main.py
```

## How to install
Installation tested are not fully tested end to end please let me know if anything does not work as I remember.

Installing dl-nhltv is not so much an installation but just a clone/copy of whats on github. 
1) click on 'code' tab
2) donwload file
3) exctract content in folder of your choice.
4) follow previous *Steps to get it working once installed...*

You wont be able to use it until you followed steps below : 

### OS X > 10.9
You probably want to be a developer for this on osx as its rather painfull at the moment. 
In a nutshell you need aria2 and ffmpeg. Python 2.7 and openssl is already there. 

*Background*
Python should already be installed but you may also need to have some additional python modules to install.
Python's package manager is called pip. 
pip can install packages for your python version you are using. We also need some non python unix commands like aia2c and ffmpeg that are not installeable via pip but can be installed painfully individual or comfortable via homebrew. 
homebrew can also install some python modules. Homebrew is also a sort of package manager but since its dealing with binaries you need to have a xcode/development environment setup in order to compile C-code. Mixing package managers can end up in a mess so below instructions will settle with homebrew

1) Follow homebrew install howto of your choice like:
https://www.howtogeek.com/211541/homebrew-for-os-x-easily-installs-desktop-apps-and-terminal-utilities/

2) Install dependencies
```
brew install aria2 ffmpeg
```
note that ffmpeg will take some time as its compiled from scratch. 
Once done you should be able to run aria2 ro ffmpeg in the terminal window. 

### Linux
On linux this should be rather easy. Havent tried. Only painfull thing could be the python version.
You need python 2.7 or higher. Might want to try 3 as some distries have 2.6 its apparently easier with python3 

#### Debian based
note: havent tried this pure guesswork 
1) install aria2
```
sudo apt-get install aria2 ffmpeg
```
2) install ffmpeg follow howto of your choice like
https://www.assetbank.co.uk/support/documentation/install/ffmpeg-debian-squeeze/ffmpeg-debian-jessie/

3) install python3
```
sudo apt-get install python3
```

#### Red Hat based
note: havent tried this pure guesswork RHEL likes its python2.6 as its system version so you need to keep that. 

1) install aria2
```
sudo yum install aria2 ffmpeg
```
2) install ffmpeg follow howto of your choice like
https://www.assetbank.co.uk/support/documentation/install/ffmpeg-debian-squeeze/ffmpeg-debian-jessie/

3) install python2.7 or try python 3
Try a yum install python3
```
sudo yum install python3
```
# Running it

When it runs it will check the nhl.tv servers for a new game for your team and if it finds it then it will download it. Then after it downloads it will do a loop and start looking for the next game. It saves the id of the last game so if you aren't getting the results you expect then take a look at the settings.json file and set the game id manually to be lower than the gameid you want to download.

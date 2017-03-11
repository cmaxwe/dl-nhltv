# dl-nhltv
Download NHL.tv Streams with up to 720p60 and remove the commercial breaks

## Requirements:
* *You need A offical NHL.tv account to run this script! This is not for free!*
* Mac or Linux. Sorry Windows users! You could maybe run it through Cygwin?
* python 2.7, aia2c, openssl, ffmpeg

## Steps to get it working once installed...

1. Set your username in the globals.py file
2. Set your password in the globals.py file
3. Set the team id in the globals.py (see comment block below for id) 
4. Set your quality in the globals.py file (or leave it at 5000k)

## Usage:
```
python2.7 main.py
```

# How to install
dl-nhltv is a python2.7 script that needs ffmpeg and aria2.

## OS X > 10.9 
You can install from precompiled binaries for from source 

### From source 
You probably want to be a developer for this. 

* Press Command+Space and type Terminal and press enter/return key.
* Run in Terminal app:

#### Install apples OS X command line development tools:
* Run command below in Terminal window: 
```
sudo xcode-select --install
```
* Click “install” button 
* Click  “Agree” on next window
* Wait for the command to finish.

#### Install homebrew:
* Run command below in Terminal window: 
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
#### Install aria2 and ffmpeg with homebrew
* Run command below in Terminal window: 
```
brew install aria2 ffmpeg
```
Note: Installation of ffmpeg will take some time as its compiled from scratch.
Once done you should be able to run aria2 or ffmpeg in the Terminal window but you probably need to start a new Terminal.

### Install from binary:
We are going to download dl-nhltv and ffmpeg and put them both into the same folder
We are going to install aria2c and start a new Terminal window. 

#### Get dl-nhltv source from github:
* Open page https://github.com/cmaxwe/dl-nhltv
* Click “Code” tab
* Click “Clone or Download” 
* Click “Download ZIP”  Open with “Archive Utility”
* Once downloaded extract dl-nhltv-master.zip
* Move extracted folder to a location where you want to run dl-nhltv from 

#### Get ffmpeg binary
* Go to http://evermeet.cx/pub/ffmpeg/
* Find the dmg file with the highest version number like “ffmpeg-3.2.4.dmg”
* Download and Open with DiskImageMounter
* Copy ffmpeg fie into same folder dl-nhltv-master

#### Get aria2 binary package and install it 
* Go to http://mac.softpedia.com/get/Internet-Utilities/aria2.shtml
* Click “DOWNLOAD” top left corner
* Click either “External Mirror” or “Softpedia Secure Download (US)”
* DONT CLICK ANYTHING! wait for the download !
* In Downloads right click on the  aria2.pkg file and select “open” 
* Click install and authenticate. 

Note: you have auto start a new Terminal window to work with aria2c !

## On Linux
On Linux this should be rather easy. Havent tried. Only painfull thing could be the python version.
You need python 2.7 or higher. Might want to try 3 as some distries have 2.6 its apparently easier with python3 

### Debian based
 
#### Install aria2 
```
sudo apt-get install aria2 ffmpeg
```
For some distributions install ffmpeg follow howto of your choice like

https://www.assetbank.co.uk/support/documentation/install/ffmpeg-debian-squeeze/ffmpeg-debian-jessie/


### Red Hat based
note: havent tried this pure guesswork RHEL likes its python2.6 as its system version so you need to keep that. 

1) install aria2
```
sudo yum install aria2 ffmpeg
```
For some distributions install ffmpeg follow howto of your choice like

https://www.assetbank.co.uk/support/documentation/install/ffmpeg-debian-squeeze/ffmpeg-debian-jessie/

## Configure dl-nhltv
* In Finder go to your dl-nhltv-master folder 
* Edit “globals.py”
* Configure username and password of your NHLTV account
USERNAME = ""
PASSWORD = ""
* Configure your team, see full list below TEAMID entry
TEAMID = "17"
* save changes and close globals.py

Note: Make sure to keep the formatting and all settings surrounded by quotes. 
OS X TextEdit is messing up the quotes by turning normal up quotes into some special up-quotes that python does not understand. On OSX You might want to use the sublime text editor instead see https://www.sublimetext.com/

## Run dl-nhltv
* Press Command+Space and type Terminal and press enter/return key.
* Run in Terminal app
* type “cd” and hit space then drag and drop your dl-nhltv-master folder into the Terminal window
* Hit enter
* Run 
```
python2.7 main.py 
```

# How dl-nhltv works 
When it runs it will check the nhl.tv servers for a new game for your team and if it finds it then it will download it. Then after it downloads it will do a loop and start looking for the next game. It saves the id of the last game so if you aren't getting the results you expect then take a look at the settings.json file and set the game id manually to be lower than the gameid you want to download.

## Files and folders
dl-nhltv downloads the parts of a stream into a temp/ subfolder below its source code. 
Per game you have a different log file for the download.
You can watch the progress of the download by looking into the temp folder.

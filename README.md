# dl-nhltv
Download NHL.tv Streams with up to 720p60 and remove the commercial breaks

## Requirements:
* *You need A offical NHL.tv account to run this script! This is not for free!*
* Mac or Linux. Sorry Windows users! You could maybe run it through Cygwin?
* python 2.7, aia2c, openssl, ffmpeg


## Usage:
```
usage: nhltv.py [-h] -t TEAMID [-u USERNAME] [-p PASSWORD] [-q QUALITY]
                [-d DOWNLOAD_FOLDER] [-r] [-m]

nhltv.py: Download NHL TV

optional arguments:
  -h, --help            show this help message and exit
  -t TEAMID, --team TEAMID
                        Team ID i.e. 17 or DET or Detroit
  -u USERNAME, --username USERNAME
                        User name of your NHLTV account
  -p PASSWORD, --password PASSWORD
                        Password of your NHL TV account
  -q QUALITY, --quality QUALITY
                        is highest by default you can set it to 5000, 3500,
                        2500, 1800, 1200, 800, 450
  -d DOWNLOAD_FOLDER, --download_folder DOWNLOAD_FOLDER
                        Output folder where you want to store your final file
                        like $HOME/Desktop/NHL/
  -r, --retry           Usually works fine without, Use this flag if you want
                        it perfect
  -m, --mobile_video    Set this to also encode video for mobile devices
```


# How to install
nhltv is a python2.7 script that needs ffmpeg and aria2.

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
We are going to download dl-nhltv 
We are going to download ffmpeg pre-build binary and put it into /usr/local/bin as root user 
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
* While on Finder User keyboard shortcut Apple+Shift+G to got to folder /usr/local/
* Authenticate with password (you need to do that a few times)
* create a new folder in /usr/local/ called "bin" (authenticate)
* change into folder bin
* drag and grop ffmpeg binary to the /usr/local/bin folder

Verify by opening a new Terminal window and type in 
```
ffmpeg -h
```
You shoudl see ffmpeg short help printed

#### Get aria2 binary package and install it 
* Go to http://mac.softpedia.com/get/Internet-Utilities/aria2.shtml
* Click “DOWNLOAD” top left corner
* Click either “External Mirror” or “Softpedia Secure Download (US)”
* DONT CLICK ANYTHING! wait for the download !
* In Downloads right click on the  aria2.pkg file and select “open” 
* Click install and authenticate. 

Verify by starting a new Terminal window and type in 
```
aria2c -h
```
You should get aria2c's help printed


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
python2.7 nhltv.py -t Detroit -u yourNhlUserName -p yourNhlPassword
```
Note: your username and password gets stored in settings.json folder so you don't need to flash it on the comamnd line everyt time.

# How dl-nhltv works 
When it runs it will check the nhl.tv servers for a new game for your team and if it finds it then it will download it. Then after it downloads it will do a loop and start looking for the next game. It saves the id of the last game so if you aren't getting the results you expect then take a look at the settings.json file and set the game id manually to be lower than the gameid you want to download. It also saves the username and password in the settings.json file

## Files and folders
dl-nhltv downloads the parts of a stream into a temp/ subfolder below its source code. 
Per game you have a different log file for the download.
You can watch the progress of the download by looking into the temp folder.

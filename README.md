# dl-nhltv
Download NHL.tv Streams and remove the commercial breaks

Steps to get it working...

1. Set your username in the globals.py file
2. Set your password in the globals.py file
3. Set your quality in the globals.py file (or leave it at 5000k)
4. Set the team id in the globals.py

If for step 4 you don't know your team id then load the nhl.tv json and find it in there...
URL for the json: 
http://statsapi.web.nhl.com/api/v1/schedule?expand=schedule.teams,schedule.linescore,schedule.scoringplays,schedule.game.content.media.epg&startDate=2016-02-10&endDate=2016-04-10&site=en_nhl&platform=playstation

Dependencies:
-aria2c
-openssl
-python 2.7
-ffmpeg

To run it you need to do something like this...
python ./main.py

When it runs it will check the nhl.tv servers for a new game for your team and if it finds it then it will download it. Then after it downloads it will do a loop and start looking for the next game.

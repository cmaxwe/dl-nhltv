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
1. aria2c
2. openssl
3. python 2.7
4. ffmpeg

To run it you need to do something like this...
python ./main.py
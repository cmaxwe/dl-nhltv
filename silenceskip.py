from globals import *


def silenceSkip(input, output):
	tprint("Analyzing " + input + " for silence.")
	command = "ffmpeg -y -nostats -i " + input + " -af silencedetect=n=-50dB:d=10 -c:v copy -c:a libmp3lame -f mp4 /dev/null"
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	pi = iter(p.stdout.readline, b'')
	marks = []
	marks.append('0')
	for line in pi:
		if('silencedetect' in line):
			start_match = re.search(r'.*silence_start: (.*)',line, re.M|re.I)
			end_match = re.search(r'.*silence_end: (.*) \|.*',line, re.M|re.I)
			if(start_match != None and start_match.lastindex == 1):
				marks.append(start_match.group(1))
				#tprint("Start: " + start_match.group(1))
			if(end_match != None and end_match.lastindex == 1):
				marks.append(end_match.group(1))
				#tprint("End: " + end_match.group(1))
	# If it is not an even number of segments then add the end point. If the last silence goes
	# to the endpoint then it will be an even number.
	if(len(marks)%2 == 1):
		marks.append('end')

	# Make a temp dir
	command = 'mkdir ./temp'
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	tprint("Creating segments.")
	seg = 0
	# Create segments
	for i in range(0,len(marks)):
		if(i%2==0):
			if(marks[i+1] != 'end'):
				seg = seg + 1
				length = float(marks[i+1]) - float(marks[i])
				command = 'ffmpeg -y -nostats -i ' + input + ' -ss ' + str(marks[i]) + ' -t ' + str(length) + ' -c:v copy -c:a copy ./temp/cut' + str(seg) + '.mp4'
			else:
				seg = seg + 1
				command = 'ffmpeg -y -nostats -i ' + input + ' -ss ' + str(marks[i]) + ' -c:v copy -c:a copy ./temp/cut' + str(seg) + '.mp4'
			subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	# Create file list
	file = open("./temp/concat_list.txt", "w")
	for i in range(1,seg+1):
		file.write("file\t" + 'cut' + str(i) + '.mp4\n')
	file.close()

	command = 'ffmpeg -y -nostats -f concat -i ./temp/concat_list.txt -c copy ' + output
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()
	tprint("Merging segments back to single video and saving: " + output)

	# Erase temp
	command = 'rm -rf ./temp'
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

	# Erase orig file
	command = 'rm ' + input
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)	
from globals import *

def download_nhl(url, outFile):
	tprint("Starting Download: " + url)
	download_options = " --load-cookies=cookies.txt --log='download.log' --log-level=notice --quiet=true --retry-wait=120 "

	# Pull url_root
	url_root = re.match('(.*)master_tablet60.m3u8',url, re.M|re.I).group(1)

	# Create a temp directory
	command = 'mkdir ./temp'
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	# Create the keys directory
	command = 'mkdir ./temp/keys'
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()	
	
	# Get the master m3u8
	command = 'aria2c -o temp/master.m3u8' + download_options + url
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	# Parse the master and get the quality URL
	command = 'cat ./temp/master.m3u8'
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	pi = iter(p.stdout.readline, b'')
	quality_url = ''
	for line in pi:
		if(QUALITY + 'K' in line):
			quality_url = url_root + line

	# Get the m3u8 for the quality
	command = 'aria2c -o temp/input.m3u8' + download_options + quality_url
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	# Parse m3u8 
	#Create files
	download_file = open("./temp/download_file.txt", "w")
	quality_url_root = re.search(r'(.*/)(.*)',quality_url, re.M|re.I).group(1)

	command = 'cat ./temp/input.m3u8'
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	pi = iter(p.stdout.readline, b'')
	ts_number = 0
	key_number = 0
	cur_iv = 0
	decode_hashes = []

	for line in pi:
		if('#EXT-X-KEY' in line):
			# Incremenet key number
			key_number = key_number + 1

			# Pull the key url and iv
			in_line_match = re.search(r'.*"(.*)",IV=0x(.*)',line, re.M|re.I)
			key_url = in_line_match.group(1)
			cur_iv = in_line_match.group(2)

			# Add file to download list
			download_file.write(key_url + '\n')
			download_file.write(' out=temp/keys/' + str(key_number) + '\n')
			
		elif('.ts\n' in line):
			# Increment ts number
			ts_number = ts_number + 1
			
			# Make alternate uri
			alt_quality_url_root = quality_url_root
			if('-l3c.' in alt_quality_url_root):
				alt_quality_url_root = alt_quality_url_root.replace('-l3c.', '-akc.')
			else:
				alt_quality_url_root = alt_quality_url_root.replace('-akc.', '-l3c.')

			# Add file to download list
			download_file.write(quality_url_root + line.strip('\n') + '\t' + alt_quality_url_root + line)
			download_file.write(' out=temp/' + str(ts_number) + '.ts\n')

			# Add to decode_hashes
			decode_hashes.append({'key_number': str(key_number), 'ts_number': str(ts_number), 'iv': str(cur_iv)})
	p.wait()
	download_file.close()

	# User aria2 to download the list
	command = 'aria2c -i ./temp/download_file.txt -j 10 ' + download_options
	p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	# Create the concat file
	concat_file = open("./temp/concat.txt", "w")

	# Iterate through the decode_hashes and run the decoder function
	for dH in decode_hashes:
		cur_key = 'blank'
		key_val = ''

		# If the cur_key isn't the one from the has then refresh the key_val
		if(cur_key != dH['key_number']):
			# Extract the key value
			command = 'xxd -p ./temp/keys/' + dH['key_number']
			p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
			pi = iter(p.stdout.readline, b'')
			for line in pi:
				key_val = line.strip('\n')
				cur_key = dH['key_number']
			p.wait()

		# Decode TS
		command = 'openssl enc -aes-128-cbc -in "./temp/' + dH['ts_number'] + '.ts" -out "./temp/' + dH['ts_number'] + '.ts.dec" -d -K ' + key_val + ' -iv ' + dH['iv']
		subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

		# Move decoded files over old files
		command = 'mv ./temp/' + dH['ts_number'] + '.ts.dec ./temp/' + dH['ts_number'] + '.ts'
		subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

		# Add to concat file
		concat_file.write('file ' + dH['ts_number'] + '.ts\n')

	# close concat file
	concat_file.close()

	# merge to single
	command = 'ffmpeg -y -nostats -loglevel 0 -f concat -i ./temp/concat.txt -c copy -bsf:a aac_adtstoasc ' + outFile
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	# delete the old directory
	command = 'rm -rf ./temp'
	subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

	return





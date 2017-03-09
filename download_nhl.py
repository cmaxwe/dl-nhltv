from globals import *
import re
import subprocess
import os

def remove_lines_without_errors(errors):
    # Open download file
    download_file = open("./temp/download_file.txt", "r+")
    download_file_lines = download_file.readlines()

    download_file.seek(0)
    writeNext = False
    for line in download_file_lines:
        for error in errors:
            # For each error check to see if it is in the line
            # If it is then write that line and the next one
            if(error in line):
                download_file.write(line)
                writeNext = True
            if(writeNext and 'out=temp/' in line):
                download_file.write(line)
                writeNext = False
    download_file.truncate()
    download_file.close()

def redo_broken_downloads(outFile):
    DOWNLOAD_OPTIONS = " --load-cookies=cookies.txt --log='" + outFile + "_download.log' --log-level=notice --quiet=true --retry-wait=1 --max-file-not-found=5 --max-tries=5 --header='Accept: */*' --header='Accept-Language: en-US,en;q=0.8' --header='Origin: https://www.nhl.com' -U='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36' --enable-http-pipelining=true --auto-file-renaming=false --allow-overwrite=true "

    logFileName = outFile + '_download.log'

    # Set counters
    lastErrorCount = 0
    lastLineNumber = 0

    while(True):
        # Loop through log file looking for errors
        logFile = open(logFileName, "r")
        startReading = False
        errors = []
        curLineNumber = 0
        for line in logFile:
            curLineNumber = curLineNumber + 1
            if(curLineNumber > lastLineNumber):
                # Is line an error?
                if('[ERROR]' in line):
                    error_match = re.search(r'/.*K/(.*)',line, re.M|re.I).group(1)
                    errors.append(error_match)
        lastLineNumber = curLineNumber
        logFile.close()

        if(len(errors) > 0):
            tprint('Found ' + str(len(errors)) + ' download errors.')
            if(lastErrorCount == len(errors)):
                tprint('Same number of errrors as last time so waiting 10 minutes')
                time.sleep(60 * 10)
            remove_lines_without_errors(errors)
            
            tprint('Trying to download the erroneous files again...')
            
            # User aria2 to download the list
            command = 'aria2c -i ./temp/download_file.txt -j 20 ' + DOWNLOAD_OPTIONS
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()
            
            lastErrorCount = len(errors)
        else:
            break


def download_nhl(url, outFile):
    DOWNLOAD_OPTIONS = " --load-cookies=cookies.txt --log='" + outFile + "_download.log' --log-level=notice --quiet=true --retry-wait=1 --max-file-not-found=5 --max-tries=5 --header='Accept: */*' --header='Accept-Language: en-US,en;q=0.8' --header='Origin: https://www.nhl.com' -U='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36' --enable-http-pipelining=true --auto-file-renaming=false --allow-overwrite=true "
    tprint("Starting Download: " + url)
    
    # Pull url_root
    url_root = re.match('(.*)master_tablet60.m3u8',url, re.M|re.I).group(1)

    # Create the temp and keys directory
    if not os.path.exists('./temp/keys'):
        os.makedirs('./temp/keys')
    
    # Get the master m3u8
    command = 'aria2c -o temp/master.m3u8' + DOWNLOAD_OPTIONS + url
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
    command = 'aria2c -o temp/input.m3u8' + DOWNLOAD_OPTIONS + quality_url
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
    tprint("starting download of individual video files")
    command = 'aria2c -i ./temp/download_file.txt -j 20 ' + DOWNLOAD_OPTIONS
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

    # Repair broken downloads if necessary
    if RETRY_ERRORED_DOWNLOADS:
        redo_broken_downloads(outFile)

    # Create the concat file
    concat_file = open("./temp/concat.txt", "w")

    # Iterate through the decode_hashes and run the decoder function
    tprint("Decode video files")
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
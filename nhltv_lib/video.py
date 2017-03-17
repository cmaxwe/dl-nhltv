import subprocess
from nhltv_lib.common import tprint


def reEncode(inputFile, outputFile):
    # command_pass1 = 'ffmpeg -y -nostats -i ' + inputFile + ' -r 30 -vf scale=640x360 -c:v libx265 -preset fast -crf 24 -pass 1 -codec:a copy -f mp4 /dev/null'
    command_pass2 = 'ffmpeg -y -nostats -i ' + inputFile + ' -r 30 -vf scale=640x360 -c:v libx265 -preset slow -x265-params bframes=0:crf=24:b-adapt=0 -codec:a opus -b:a 48k ' + outputFile + '.mkv'
    # subprocess.Popen(command_pass1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()
    # tprint('Pass 1 Complete!')
    subprocess.Popen(command_pass2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()
    tprint('Pass 2 Complete!')

    tprint('Splitting...')
    # Create first hour
    command = 'ffmpeg -y -t 3600 -nostats -i ' + outputFile + '.mkv -c:v copy -codec:a copy ' + outputFile + '_start.mkv'
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()
    # Create rest
    command = 'ffmpeg -y -ss 3600 -nostats -i ' + outputFile + '.mkv -c:v copy -codec:a copy ' + outputFile + '_end.mkv'
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).wait()

    # Clean up
    command = 'rm ffmpeg2pass-0.log'
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    command = 'rm ' + outputFile + '.mkv'
    subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

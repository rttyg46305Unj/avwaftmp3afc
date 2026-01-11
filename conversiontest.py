from os import system as command
from sys import argv as arguments
from os import listdir as filelist
from os import name as ostype

try:
    import zipfile
except:
    command('python -m pip install zipfile')
    import zipfile

true = True
false = False
replace = false

def getvalflag(flag): # Gets a flag form the arguments.
    if len(flag)>1: # Very simple dash stuff
        dashes = '--'
    else:
        dashes = '-'
    return(arguments[((arguments.index(dashes+flag))+1)]) # Return the value of said flag

if '--name' in arguments: # Get name or folder
    soundname = getvalflag('name')
elif '-b' in arguments:
    bunch = true
    bunchdir = getvalflag('b')
elif '--zip' in arguments:
    bunch = true
    zip1 = getvalflag('zip')
    with zipfile.ZipFile(zip1, 'r') as zipf:
        zipf.extractall(f'{zip1}-unzp')
    bunchdir = f'{zip1}-unzp'
else:
    print('no name or smth like that')


if '--forcesample' in arguments: # Sample rate (not bitrate)
    samplerate = getvalflag('forcesample')
else:
    samplerate = command(f'ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of default=noprint_wrappers=1:nokey=1 {soundname}.wav')


if '-c' in arguments: # The "c" flag makes it mono. 
    channels = 1
else:
    channels = 2

if '--bit' in arguments: # Bitrate in kilobits.
    bitrate = getvalflag('bit')
else:
    bitrate = 48

if '--replace' in arguments: # Self explanatory. 
    replace = true

if bunch:
    wav_files = []
    # Not the best solution for this problem
    for filename in filelist(bunchdir):
        if filename.endswith('.wav'):
            wav_files.append(filename.split('.')[0])
    for sidx in wav_files:
        command(f'ffmpeg -i {bunchdir}/{sidx}.wav -vn -ar {samplerate} -ac {channels} -b:a {bitrate}k {bunchdir}/{sidx}.mp3') # Do conversion
        if replace:
            if ostype=='nt':
                print(f'deleting {sidx}')
                command(f'del {bunchdir}\\{sidx}.wav')
            else:
                command(f'rm {bunchdir}/{sidx}.wav')
        
        
else:        
    command(f'ffmpeg -i {soundname}.wav -vn -ar {samplerate} -ac {channels} -b:a {bitrate}k {soundname}.mp3') # Do conversion
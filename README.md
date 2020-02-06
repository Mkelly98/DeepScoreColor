Aggregation of some tools and scripts to perform some visual, musical, and color analysis for the Robotic Musicianship lab.

-----

scenedetect: download from https://github.com/Breakthrough/PySceneDetect

run "scenedetect -i inthemoodforlove.mp4 -o moodforloveClips detect-content split-video" to split a video (ex. inthemoodforlove.mp4) into a directory of clips (ex. moodforloveClips)

-----

frames.py: Converts a single video into a directory of frames

Run 'python frames.py' 
and when prompted, type the video's filename
once the terminal prints that the process is complete the frames will be in the new directory

ex. python Frames.py

filename: inthemoodforlove.mp4

Frame conversion completed

(the frames are in inthemoodforlove_frames directory)

-----

dirFrames.py: Converts a directory of videos into a directory of frames

Run 'python dirFrames.py' 
and when prompted, type the directory's name and then the name you would like for the main directory
once the terminal prints that the process is complete the frames will be in the new directory

ex. python dirFrames.py

filename: moodforloveCips

title: moodforlove

Frame conversion completed

(the frame subdirectories are in moodforlove_frames directory)

-----
colorific : Used to obtain the dominant color palette from frames, code was edited to provide RGB values and color names in a csv file. Download from https://github.com/99designs/colorific and replace the palette.py file with the one in this repository
   
Steps:
- activate a virtual environment
- use the command "pip install colorific"
- use the command "pip install webcolors==1.3"
- save this version of the "pallette.py" code in the colorific file in your virtual environment (aka replace the orignal)
   - location example: YourVirtualEnv/lib/Python3.6/site-packages/colorific
- save this version of the "webcolors.py" code in the site-packages file in your virtual environment (aka replace the orignal)
   - location example: YourVirtualEnv/lib/Python3.6/site-packages/colorific



Run "find moodforlove_frames '*.jpg' | colorific" to create the csv file of the color palette from the folder (ex. moodforlove_frames)

-----

run-music-extractor.sh: run essentia's [music extractor](https://essentia.upf.edu/documentation/streaming_extractor_music.html) on an audio file.

Usage: `./run-music-extractor \[path/to/file]`

Produces an output text file containing the extracted features.

Make sure this file is in the same directory as the extracted essentia-extractors-v2.1_beta2-linux-x86_64.tar.gz directory.

Follow directions [here](https://essentia.upf.edu/documentation/extractors_out_of_box.html) to install Essentia's prebuilt feature extractor binaries, or use
install-essentia-extractor.sh (described below).

-----
install-extractors.sh: install essentia's [extractors](https://essentia.upf.edu/documentation/streaming_extractor_music.html) and uncompresses them into the current working directory.

Usage: `./install-essentia-extractor -os <operating system>`

The `-os` argument can be one of the following: 'mac', 'linux-i686', or 'linux-x86', depending on your operating system.


-----
run-sound-extractor.sh: run essentias [freesound extractor](https://essentia.upf.edu/documentation/freesound_extractor.html) on an audio file.
Usage: `./run-sound-extractor -os <operating system>`
The `-os` argument can be one of the following: 'mac', 'linux-i686', or 'linux-x86', depending on your operating system.

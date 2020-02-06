#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Missing path to audio file. Usage: ./run-sound-extractor [path/to/audio/file]"
else
   audio_path=$1
   fname=${audio_path##*/}
   essentia-extractors-v2.1_beta2/streaming_extractor_freesound ${audio_path} ${fname%.*}_sound_analysis.txt
    
fi

#!/bin/bash

function usage {
    cat << EOF

Usage: ./install-music-extractor -os <operating system>

Values of <operating system> can be 'mac', 'linux-x86', or 'linux-i686'. -os is a required argument.

Downloads and extracts essentia streaming music extractors in the current working directory.
EOF
    exit 1
}

if [ "$#" -ne 2 ]; then 
    usage;
fi

if [ "$1" != "-os" ]; then 
    usage;
fi

OS="$2"

if [ $OS == "mac" ]; then
    echo "installing extractors..."
    wget https://essentia.upf.edu/documentation/extractors/essentia-extractors-v2.1_beta2-osx-x86_64.tar.gz
    tar xvzf essentia-extractors-v2.1_beta2-osx-x86_64.tar.gz
    echo "done!"

elif [ $OS == "linux-i686" ]; then
    echo "installing extractors..."
    wget https://essentia.upf.edu/documentation/extractors/essentia-extractors-v2.1_beta2-linux-i686.tar.gz
    tar xvzf essentia-extractors-v2.1_beta2-linux-i686.tar.gz
    echo "done!"

elif [ $OS == "linux-x86" ]; then
    echo "installing extractors..."
    wget https://essentia.upf.edu/documentation/extractors/essentia-extractors-v2.1_beta2-linux-x86_64.tar.gz
    tar xvzf essentia-extractors-v2.1_beta2-linux-x86_64.tar.gz
    echo "done!"

else
    usage;
fi



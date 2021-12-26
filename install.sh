#!/bin/bash

BASEDIR=$(dirname `realpath $0`)

echo "Installing Dependencies";
sudo apt install -y python3 python3-pyglet python3-future mpg123;

#Let's use python3 for the program
cd ${BASEDIR};
sed -i 's[^#!/usr/bin/env python$[#!/usr/bin/env python3[g' brainworkshop.py;
chmod +x brainworkshop.py;

echo "Copying files to /opt and setting up desktop file";
sudo mkdir -p /opt/;
sudo cp -r ${BASEDIR} /opt/;
sudo ln -s /opt/brainworkshop/brainworkshop.py /usr/local/bin/brainworkshop > /dev/null 2>&1;
sudo mkdir -p /usr/local/share/pixmaps /usr/local/share/applications;
sudo cp /opt/brainworkshop/icons/brainworkshop.png /usr/local/share/pixmaps;
sudo cp /opt/brainworkshop/brainworkshop.desktop /usr/local/share/applications;

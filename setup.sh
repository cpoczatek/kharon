#!/usr/bin/bash

# let's install pip
sudo apt-get -y install python-pip

# dependencies for 'cryptography' python package
sudo apt-get -y install build-essential libssl-dev libffi-dev python-dev

# install paramiko, should install dependency'cryptography'
sudo pip install paramiko

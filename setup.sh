#!/bin/bash

WORKDIR=$PWD

# install intltool
sudo apt-get install intltool

# install mwget
cd /usr/local/src
sudo wget http://jaist.dl.sourceforge.net/project/kmphpfm/mwget/0.1/mwget_0.1.0.orig.tar.bz2
sudo tar -xjvf mwget_0.1.0.orig.tar.bz2
cd mwget_0.1.0.orig
sudo ./configure
sudo make
sudo make install

cd $WORKDIR

#!/bin/bash

# This is the MAIN SCRIPT for downloading, setting up, and running the Beasley Weather Station 
# on the BeagleBoneGreen or server.
# This script will figure out which hardware you are running and either setup the BBG OR server

# definitions
USER=badger
USER_HOME_DIR=/home/$USER
USER_BEASLEY_DIR=$USER_HOME_DIR/beasley-weather-station/
BBG_SCRIPTS_DIR=$USER_BEASLEY_DIR/bbg/scripts
SERVER_SCRIPTS_DIR=$USER_BEASLEY_DIR/server/scripts
BBG_SETUP_SCRIPT=setupBBG.sh
SERVER_SETUP_SCRIPT=setupServer.sh

# exit as soon as there is an error
set -e

# step 1
echo -e "\nCreating main user (badger) and file structure..."
mkdir -p $USER_BEASLEY_DIR
if [ `id -u $USER` ]
then
	echo "User $USER already exists (this is good)"
else
	echo "If if prompts for password and Full name, make it \"$USER\" and press \"Enter\" for everything else."
	adduser --quiet $USER --home $USER_HOME_DIR
	echo "Adding user $USER complete."
fi

# step 2
echo -e "\nDownloading all necessary git repos for scripts and config files..."
cd $USER_HOME_DIR

while true; do
    read -p "Do you wish to reinstall git repos? [y/n]" yn
    case $yn in
        [Yy]* )
        	read -p "Clear all existing repos in $USER folder? YES=[ENTER] or NO=CTRL-C"
			rm -rf $USER_BEASLEY_DIR
			mkdir -p $USER_BEASLEY_DIR
			cd $USER_BEASLEY_DIR
			git clone https://github.com/beasley-weather/beasley-weather-station.git # need to redownload self becase I just rm'ed myself
			git clone https://github.com/beasley-weather/server.git
			git clone https://github.com/beasley-weather/bbg.git
			git clone https://github.com/beasley-weather/data-generator.git
			git clone https://github.com/beasley-weather/extract-data.git
			git clone https://github.com/beasley-weather/project-tracking.git
			git clone https://github.com/beasley-weather/libdb.git
			echo "Done downloading all beasley-weather-station repos." 
			break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo -e "\nRecursively change all file permissions to \"$USER\"..."
chown -R $USER:$USER $USER_HOME_DIR

echo -e "\nMake sure user [" $USER "] is able to ssh into this system..."
# https://askubuntu.com/questions/16650/create-a-new-ssh-user-on-ubuntu-server
sh -c 'echo "AllowUsers " $USER >> /etc/ssh/sshd_config'

echo -e "\nCheck hardware architecture to see if I am running on a BeagleBoneGreen or server..."
#if [ `arch` == "armhf" ]
while true; do
    read -p "Do you wish to setup the BeagleBone (b) or the Server (s) or None(n)? [b/s/n]" bs
    case $bs in
        [Bb]* )
			echo "Architecture is armhf, therefore this is a BEAGLE BONE GREEN/BLACK  and will be configured as such."
			$BBG_SCRIPTS_DIR/$BBG_SETUP_SCRIPT
			break;;
        [Ss]* ) 
			echo "Architecture is not armhf, therefore this is a SERVER and will be configured as such."
			$SERVER_SCRIPTS_DIR/$SERVER_SETUP_SCRIPT
			break;;
		[Nn]* ) 
			break;;
        * ) echo "Please answer (b) or (s) or (n).";;
    esac
done

#!/bin/sh

sudo /bin/launchctl unload -S Aqua /Library/LaunchDaemons/com.solon.uwsgi.plist
sudo /bin/launchctl load /Library/LaunchDaemons/com.solon.uwsgi.plist
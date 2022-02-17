#!/bin/bash

cat /opt/rtcds/kamioka/k1/chans/daq/*.ini | grep -e "^\[K1" | sed -e "s/\[\(.*\)\]/\1/g" > /kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/daqchannels.txt 

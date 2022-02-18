#!/bin/bash

grep -e "COMMISH" /kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/daqchannels.txt | grep -e "VIS" | sed "s/STATUS/MESSAGE/g" | xargs caget

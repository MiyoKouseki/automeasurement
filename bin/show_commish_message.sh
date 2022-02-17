#!/bin/bash

grep -e "COM" /kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/daqchannels.txt | sed "s/STATUS/MESSAGE/g" | xargs caget

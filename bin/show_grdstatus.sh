#!/bin/bash

grep -e "GRD" /kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/daqchannels.txt | grep -e "K1:GRD-VIS_.*_STATE_N" | sed "s/STATE_N/STATE_S/g" | xargs caget

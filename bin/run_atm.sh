#!/bin/bash
pushd /kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/lib
export NDSSERVER=k1nds1:8088,k1nds0:8088,k1nds2:8088
exec /home/controls/miniconda3/envs/miyoconda37/bin/python run_atm.py
popd

#!/bin/bash

OPTIC=${1:=ITMX}
STATE=${2:STANDBY}
STAGE=${3:IM}

find /kagra/Dropbox/Measurements/VIS/PLANT/* -name '*.xml' | grep ${OPTIC}_${STATE}_${STAGE} |sed -E "s/^.*_${OPTIC}_${STATE}_${STAGE}_.*_([0-9]{12})\.xml$/\1/p" | grep -v xml | sort -nr | uniq | head -n10

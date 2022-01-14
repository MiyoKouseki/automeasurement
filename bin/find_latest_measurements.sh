#!/bin/bash

latest=`bash ${AUTOMEASUREMENT_BIN_PATH}/get_latest_refnumber.sh | head -n1`
find /kagra/Dropbox/Measurements/VIS/PLANT/ -name "*${latest}.xml"

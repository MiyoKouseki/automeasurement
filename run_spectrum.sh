#!/bin/bash
#******************************************#
#     File Name: run_specrum.sh
#        Author: Takafumi Ushiba, Hirotaka Yuzurihara, Kouseki Miyo
#******************************************#

#####  User parameter
DEBUG=1

if [ $# -ne 2 ]; then
    echo "Error : this script needs the date string, such as TypeA \"2021/11/1 13:53:02 UTC\""
    echo ""
    echo "usage : autoDiaggui_SPECTRUM.sh TypeA \"2021/11/1 13:53:02 UTC\""
    exit 1
fi


sustype="$1"
FILES=`cat "templates.txt" | grep -v -e '^#' | grep "SPE_${sustype}.*.xml"`
if [ -z "$FILES" ]; then
    echo "No template files."
    exit 1
fi

#this script requires gwpy module
source ~/miniconda3/etc/profile.d/conda.sh
conda activate noiseb 

DATE_BEG="$2"
GPS_BEG=`/users/das/bin/date2gps.py "${DATE_BEG}"`
GPS_BEG_TAIL="000000000"

REFFILE='/users/ushiba/script/REF_SPECTRUM.txt'
REFNUM=`cat ${REFFILE}`
REFNUM=`printf "%d" ${REFNUM}`
let REFNUM=${REFNUM}+1

echo ${REFNUM}>${REFFILE}
echo "REFNUM is updated to ${REFNUM}"
let DIR=${REFNUM}/100*100
REFNUM=`printf "%04d" ${REFNUM}`

SAVE="/kagra/Dropbox/Measurements/VIS/SPECTRA"

#####  Helper function
function measurement(){
    local XML=`basename "$1" | sed -e "s/_0000/_${REFNUM}/g"`
    local NAME=`basename ${XML%.*}`
    mkdir -p ${SAVE}/${DIR}
    printf "\033[31;01m=== Running ${NAME}.xml ===\033[00m\n"
    [ ${DEBUG} = "1" ] && cmd=diag || cmd=cat
    #[ ${DEBUG} = "1" ] && cmd=cat
    ${cmd} <<EOF
open
restore ${1}
set Sync.Start = ${GPS_BEG}${GPS_BEG_TAIL}
run -w
save ${SAVE}/${DIR}/${XML}
#save ${XML}
quit
EOF
}

#####  Main process
for FILE in ${FILES}
do
    measurement ${FILE}
done

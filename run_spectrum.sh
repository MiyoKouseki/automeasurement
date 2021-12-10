#!/bin/bash
#******************************************#
#     File Name: autoDiaggui_SPECTRUM.sh
#        Author: Takafumi Ushiba, Hirotaka Yuzurihara, Kouseki Miyo
#******************************************#

#####  User parameter
DEBUG=1
FILES=`cat <<EOF | grep -v -e '^#'
#--------   File List  --------#
/users/ushiba/template/spectrum/SPE_TypeA_IP_EUL_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_IP_SENS_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_BF_EUL_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_BF_SENS_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_GAS_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_MN_EUL_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_MN_SENS_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_IM_EUL_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_IM_SENS_0000.xml
/users/ushiba/template/spectrum/SPE_TypeA_OPLEV_0000.xml
#------ End of File List ------#
EOF`

if [ $# -ne 1 ]; then
    echo "Error : this script needs the date string, such as \"2021/11/1 13:53:02 UTC\""
    echo ""
    echo "usage : autoDiaggui_SPECTRUM.sh \"2021/11/1 13:53:02 UTC\""
    exit 1
fi

#this script requires gwpy module
source ~/miniconda3/etc/profile.d/conda.sh
conda activate noiseb 

DATE_BEG="$1"
echo $DATE_BEG
GPS_BEG=`/users/das/bin/date2gps.py "${DATE_BEG}"`
GPS_BEG_TAIL="000000000"
echo "/users/das/bin/date2gps.py ""${DATE_BEG}"""
echo "DATE : $DATE_BEG"
echo "GPS : $GPS_BEG"
#exit 1

REFNUM=`cat /users/ushiba/script/REF_SPECTRUM.txt`
REFNUM=`printf "%d" ${REFNUM}`
let REFNUM=${REFNUM}+1

echo ${REFNUM}>REF_SPECTRUM.txt
let DIR=${REFNUM}/100*100
REFNUM=`printf "%04d" ${REFNUM}`

SAVE="/kagra/Dropbox/Measurements/VIS/SPECTRA"

#####  Helper function
function measurement(){
    local XML=`basename "$1" | sed -e "s/_0000/_${REFNUM}/g"`
    local NAME=`basename ${XML%.*}`
    mkdir -p ${SAVE}/${DIR}
    printf "\033[31;01m=== Running ${NAME}.xml ===\033[00m\n"
    #[ ${DEBUG} = "1" ] && cmd=diag || cmd=cat
    [ ${DEBUG} = "1" ] && cmd=cat
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

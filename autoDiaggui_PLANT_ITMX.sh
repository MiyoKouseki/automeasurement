#!/bin/bash
#******************************************#
#     File Name: autoDiaggui_PLANT_ITMX.sh
#        Author: Takafumi Ushiba
# Last Modified: 2021/10/27 18:53:00
#******************************************#

#####  User parameter
DEBUG=1
FILES=`cat <<EOF | grep -v -e '^#'
#--------   File List  --------#
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IP_TEST_L_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IP_TEST_T_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IP_TEST_Y_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IP_COILOUTF_H1_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IP_COILOUTF_H2_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IP_COILOUTF_H3_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_TEST_L_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_TEST_T_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_TEST_V_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_TEST_R_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_TEST_P_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_TEST_Y_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_COILOUTF_V1_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_COILOUTF_V2_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_COILOUTF_V3_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_COILOUTF_H1_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_COILOUTF_H2_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_COILOUTF_H3_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_F0_TEST_GAS_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_F1_TEST_GAS_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_F2_TEST_GAS_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_F3_TEST_GAS_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_BF_TEST_GAS_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_TEST_L_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_TEST_T_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_TEST_V_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_TEST_R_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_TEST_P_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_TEST_Y_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_COILOUTF_V1_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_COILOUTF_V2_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_COILOUTF_V3_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_COILOUTF_H1_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_COILOUTF_H2_0000.xml
#/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_MN_COILOUTF_H3_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IM_TEST_L_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IM_TEST_T_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IM_TEST_V_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IM_TEST_R_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IM_TEST_P_0000.xml
/users/ushiba/template/TF/ITMX/PLANT_ITMX_STATE_IM_TEST_Y_0000.xml
#------ End of File List ------#
EOF`
SAVE=/kagra/Dropbox/Measurements/VIS/PLANT

REFNUM=`cat REF_PLANT_ITMX.txt`
REFNUM=`printf "%d" ${REFNUM}`
let REFNUM=${REFNUM}+1

echo ${REFNUM}>REF_PLANT_ITMX.txt
let DIR=${REFNUM}/100*100

REFNUM=`printf "%04d" ${REFNUM}`
STATE=`caget -t K1:GRD-VIS_ITMX_STATE_S`

#####  Helper function
function measurement(){
    local XML=`basename "$1" | sed -e "s/_0000/_${REFNUM}/g" -e "s/STATE/${STATE}/g"`
    local DATE=`date +%y%m%d_%H%M%S`
    local NAME=`basename ${XML%.*}`
    printf "\033[31;01m=== Running ${NAME}.xml ===\033[00m\n"
    mkdir -p ${SAVE}/ITMX/${DIR}
    [ ${DEBUG} = "1" ] && cmd=diag || cmd=cat
    ${cmd} <<EOF
open
restore ${1}
run -w
save ${SAVE}/ITMX/${DIR}/${XML}
quit
EOF
}

#####  Main process
for FILE in ${FILES}
do
    measurement ${FILE}
    sleep 10
done

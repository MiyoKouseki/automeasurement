#!/bin/bash

if [ $# -ne 5 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo "実行するには4個の引数が必要です。" 1>&2
  exit 1
fi

# Check SUS
SUS=$1

# Check STAGE
STAGE=$2

# Check EXC
EXC=$3

# Check DOF
DOF=$4

# Check BW
BW=$5

# Check AVE
AVE=3

# Set Stages
if [ "$STAGE" = "ALL" ]; then
    STAGES=(IP BF GAS MN IM)
elif [ "$STAGE" = "TWR" ]; then
    STAGES=(IP BF GAS)
elif [ "$STAGE" = "PAY" ]; then
    STAGES=(MN IM)
else
    STAGES=${STAGE}
fi    

# Set DOFs
if [ "$DOF" = "ALL" ]; then
    DOFS=(L T Y P R V F0 F1 F2 F3 BF)
elif [ "$DOF" = "HOR" ]; then
    DOFS=(L T Y)
elif [ "$DOF" = "VER" ]; then
    DOFS=(P R V)
else
    DOFS=${DOF}
fi

# Confirmation
echo -e " \033[1;31mSupension : ${SUS}\033[0;39m"
echo -e " \033[1;31mStage     : ${STAGES[@]}\033[0;39m"
echo -e " \033[1;31mDOF       : ${DOFS[@]}\033[0;39m"
echo -e " \033[1;31mBW        : ${BW} Hz\033[0;39m"
echo -e " \033[1;31mAVE       : ${AVE}\033[0;39m"
read -p "(y/n):" YN
if [ "${YN}" = "" ]; then
    DEBUG=0
elif [ "${YN}" = "y" ]; then
    DEBUG=1
else
    echo "you chose ${YN}. Stop. "
  exit 1;
fi

# Check if other workers measure the same suspension.
echo "OK. No one measure ${SUS}"

# Set Refnumber
outputs_dir=/kagra/Dropbox/Measurements/VIS/PLANT/${SUS}/`date +%Y/%m`
if [ ! -e ${outputs_dir} ]; then
  mkdir -p ${outputs_dir}
fi
refnum=`date +%Y%m%d%H%M`

# Check STATE
STATE=`caget -t K1:GRD-VIS_${SUS}_STATE_S` 
if [ $? -gt 0 ]; then
    exit # fixme
fi

# Run 
for STAGE in ${STAGES[@]}; do
    for DOF in ${DOFS[@]}; do       	
	output=${outputs_dir}/PLANT_${SUS}_${STATE}_${STAGE}_${EXC}_${DOF}_${refnum}.xml
	run_plant ${SUS} ${STAGE} ${EXC} ${DOF} ${BW} ${output} ${DEBUG} ${STATE}
    done
done

# Open the latest XML file with diaggui
#latest=`ls -rt ${outputs_dir} | grep xml |tail -n 1`
#[ ${DEBUG} = "1" ] && cmd=diaggui || cmd=echo
#$cmd $outputs_dir/$latest
#ls $outputs_dir | grep $refnum | xargs -l -P 3 $cmd

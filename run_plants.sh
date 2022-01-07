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
    DOFS=(L T Y P R V)
elif [ "$DOF" = "HOR" ]; then
    DOFS=(L T Y)
elif [ "$DOF" = "VER" ]; then
    DOFS=(P R V)
else
    DOFS=${DOF}
fi

# Confirmation
echo "Supension : ${SUS}"
echo "Stage     : ${STAGES[@]}"
echo "DOF       : ${DOFS}"
#echo "BW        : ${BW} Hz"
echo "AVE       : ${AVE}"
read -p "(Enter):" YN
if [ "${YN}" = "" ]; then
    echo ""
else
    echo "you chose ${YN}. Stop. "
  exit 1;
fi

# Set Refnumber
outputs_dir=/kagra/Dropbox/Measurements/VIS/PLANT/${SUS}/`date +%Y/%m`
if [ ! -e ${outputs_dir} ]; then
  mkdir -p ${outputs_dir}
fi
refnum=`date +%Y%m%d%H%M`

# Run 
for STAGE in ${STAGES[@]}; do
    for DOF in ${DOFS[@]}; do       	
	output=${outputs_dir}/PLANT_${SUS}_${STATE}_${STAGE}_${EXC}_${DOF}_${refnum}.xml
	run_plant ${SUS} ${STAGE} ${EXC} ${DOF} 0.1 ${output}
    done
done

# Open the latest XML file with diaggui
DEBUG=0
latest=`ls -rt ${outputs_dir} | grep xml |tail -n 1`
[ ${DEBUG} = "1" ] && cmd=diaggui || cmd=echo
$cmd $outputs_dir/$latest

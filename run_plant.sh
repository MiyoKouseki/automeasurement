#!/bin/bash

# ./run_tf.sh
# ./run_spectrum.sh
# ./templates/PLANT_{SUS}_{GRDSTATE}_{STAGE}_{EXC}_{DOF}_{TIME}.xml
# ./templates/SPECTRA_{SUS}_{STATE}_{STAGE}_{TIME}.xml
# ./measurements/{SUS}/{PLANT,SPECTRA}/{YYYY}/{mmdd}/*{HHMM}.xml

if [ $# -ne 5 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo "実行するには4個の引数が必要です。" 1>&2
  exit 1
fi

SUS=$1
STAGE=$2
EXC=$3
DOF=$4
BW=$5

# Fix me 
if [[ "$DOF" = "L" ]] || [[ "$DOF" = "F0" ]]; then
    exc_dof_num=0
elif [[ "$DOF" = "P" ]] || [[ "$DOF" = "F1" ]]; then
    exc_dof_num=1    
elif [[ "$DOF" = "R" ]] || [[ "$DOF" = "F2" ]]; then
    exc_dof_num=2    
elif [[ "$DOF" = "T" ]] || [[ "$DOF" = "F3" ]]; then
    exc_dof_num=3    
elif [[ "$DOF" = "V" ]] || [[ "$DOF" = "BF" ]]; then
    exc_dof_num=4    
elif [[ "$DOF" = "Y" ]]; then
    exc_dof_num=5
elif [[ "$DOF" = "H1" ]]; then
    exc_dof_num=6
elif [[ "$DOF" = "H2" ]]; then
    exc_dof_num=7
elif [[ "$DOF" = "H3" ]]; then
    exc_dof_num=8
elif [[ "$DOF" = "V1" ]]; then
    exc_dof_num=9
elif [[ "$DOF" = "V2" ]]; then
    exc_dof_num=10
elif [[ "$DOF" = "V3" ]]; then
    exc_dof_num=11   
else
    echo 'error'
    exit
fi
  

outputs_dir=./measurements/${SUS}/PLANT/`date +%Y/%m%d`
templates_dir=./templates

if [ ! -e ${outputs_dir} ]; then
  mkdir -p ${outputs_dir}
fi

_out=`caget K1:GRD-VIS_${SUS}_STATE_S`
if [ $? -gt 0 ]; then
    exit #
else
    STATE=`echo $_out | awk '{print $2}'`
fi

REFNUM=`date +%H%M`
template=${templates_dir}/PLANT_${SUS}_STATE_${STAGE}_0000.xml
output=${outputs_dir}/PLANT_${SUS}_${STATE}_${STAGE}_${EXC}_${DOF}_${REFNUM}.xml

if [ $STAGE = GAS ]; then
    STAGE=$4
    DOF=$2
fi

#
# Run
#
DEBUG=1
printf "\033[31;01m=== Running ${SUS}_${STAGE}_${EXC}_${DOF} ===\033[00m\n"
echo "open" >tmp
echo "restore "$template >>tmp
echo "set Test.BW = ${BW}">>tmp
echo "set Test.StimulusActive[${exc_dof_num}] = true">>tmp
# 複数でExcitationしないために使わないEXCチャンネルのActiveはFalseにしたほうがいい。
echo "run -w" >>tmp
echo "save "$output >> tmp
echo "quit" >> tmp
[ ${DEBUG} = "1" ] && cmd=diag || cmd=cat
$cmd < tmp


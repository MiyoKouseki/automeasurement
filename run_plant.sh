#!/bin/bash

# ./run_tf.sh
# ./run_spectrum.sh
# ./templates/PLANT_{SUS}_{GRDSTATE}_{STAGE}_{EXC}_{DOF}_{TIME}.xml
# ./templates/SPECTRA_{SUS}_{STATE}_{STAGE}_{TIME}.xml
# ./measurements/{SUS}/{PLANT,SPECTRA}/{YYYY}/{mmdd}/*{HHMM}.xml

if [ $# -ne 4 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo "実行するには4個の引数が必要です。" 1>&2
  exit 1
fi

SUS=$1
STAGE=$2
EXC=$3
DOF=$4

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

#
# Read params.txt
#
# [Memo] '#' でコメントアウト
# [Memo] 重複した場合は一つ目を読む
# [Memo] フィルターがない場合空白でも可。
# 

if [ $STAGE = GAS ]; then
    STAGE=$4
    DOF=$2
fi
exc_name=${SUS}_${STAGE}_${EXC}_${DOF}_EXC
params=(`cat params.txt|grep -v -e '^#'|grep ${exc_name}|xargs -d'\n'`)
bw=${params[1]}
amp=${params[2]}
filter=${params[3]}
exc_channel=K1:VIS-${exc_name}

#
# Run
#
DEBUG=1
printf "\033[31;01m=== Running ${exc_name} ===\033[00m\n"
echo "open" >tmp
echo "restore "$template >>tmp
echo "set Test.BW = ${bw}">>tmp
echo "set Test.StimulusChannel[0] = ${exc_channel}">>tmp
echo "set Test.StimulusAmplitude[0] = ${amp}">>tmp
echo "set Test.StimulusFilter[0] = ${filter}">>tmp
echo "run -w" >>tmp
echo "save "$output >> tmp
echo "quit" >> tmp
[ ${DEBUG} = "1" ] && cmd=diag || cmd=cat
$cmd < tmp


#!/bin/bash

# ./run_tf.sh
# ./run_spectrum.sh
# ./templates/PLANT_{SUS}_{GRDSTATE}_{STAGE}_{EXC}_{DOF}_{TIME}.xml
# ./templates/SPECTRA_{SUS}_{STATE}_{STAGE}_{TIME}.xml
# ./measurements/{SUS}/{PLANT,SPECTRA}/{YYYY}/{mmdd}/*{HHMM}.xml

if [ $# -ne 8 ]; then
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
if [ "$EXC" != "TEST" ] && [ "$EXC" != "COILOUTF" ]; then
    echo "${EXC} is a invalid excitation point."
    exit 1;
fi

# Check BW
BW=$5
if [ "$STAGE" = "BF" ]; then
    if [ "$DOF" = "Y" ]; then    
	BW=0.001
    else
	BW=0.003
    fi
elif [ "$STAGE" = "IP" ]; then
    BW=0.003
elif [ "$STAGE" = "GAS" ] || [ "$STAGE" = "IM" ] || [ "$STAGE" = "MN" ]; then
    BW=0.01
else
    echo "${STAGE} is invalid stage name."
    exit 1;
fi

# Check AVE
AVE=3

# Check output file name
output=${6}

#
STATE=${7}

# Check Template
templates_dir=/kagra/Dropbox/Measurements/VIS/scripts/automeasurement/templates
template=${templates_dir}/PLANT_${SUS}_STATE_${STAGE}_0000.xml
if [ ! -f $template ]; then
    echo 'No template file ${template}'
    exit 1;
fi

# Check DOF
DOF=$4
if [ $STAGE = GAS ]; then
    STAGE=$4
    DOF=$2
fi

# Get Excitation Channel Number
DOFNUM=`grep -e "StimulusChannel.*${SUS}_${STAGE}_${EXC}_${DOF}" $template | sed -r 's/^.*StimulusChannel\[([0-9]+)\].*$/\1/'`
isNumeric() {
  expr "$1" + 1 >/dev/null 2>&1
  if [ $? -ge 2 ]; then
    return 1
  fi
  return 0
}
if ! isNumeric ${DOFNUM} ; then
  exit 1;
fi

# Check output
if [ -f $output ]; then
    echo '${output} already exists.'
    exit 1;
fi

# Run
DEBUG=$7
printf "\033[30;01m=== Running ${SUS}_${STAGE}_${EXC}_${DOF} ===\033[00m\n"
echo "open" >tmp
echo "restore "$template >>tmp
echo "set Test.BW = ${BW}">>tmp
echo "set Test.StimulusActive[${DOFNUM}] = true">>tmp
# [Memo] 複数でExcitationしないために使わないEXCチャンネルのActiveはFalseにしたほうがいい。
echo "run -w" >>tmp
echo "save "$output >> tmp
echo "quit" >> tmp
[ ${DEBUG} = "1" ] && cmd=diag || cmd=cat
$cmd < tmp
rm tmp

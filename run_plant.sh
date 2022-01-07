#!/bin/bash

# ./run_tf.sh
# ./run_spectrum.sh
# ./templates/PLANT_{SUS}_{GRDSTATE}_{STAGE}_{EXC}_{DOF}_{TIME}.xml
# ./templates/SPECTRA_{SUS}_{STATE}_{STAGE}_{TIME}.xml
# ./measurements/{SUS}/{PLANT,SPECTRA}/{YYYY}/{mmdd}/*{HHMM}.xml

if [ $# -ne 7 ]; then
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

# Check DOF [fixme]
DOF=$4
if [[ "$DOF" = "L" ]] || [[ "$DOF" = "F0" ]]; then
    DOFNUM=0
elif [[ "$DOF" = "P" ]] || [[ "$DOF" = "F1" ]]; then
    DOFNUM=1    
elif [[ "$DOF" = "R" ]] || [[ "$DOF" = "F2" ]]; then
    DOFNUM=2    
elif [[ "$DOF" = "T" ]] || [[ "$DOF" = "F3" ]]; then
    DOFNUM=3    
elif [[ "$DOF" = "V" ]] || [[ "$DOF" = "BF" ]]; then
    DOFNUM=4    
elif [[ "$DOF" = "Y" ]]; then
    DOFNUM=5
elif [[ "$DOF" = "H1" ]]; then
    DOFNUM=6
elif [[ "$DOF" = "H2" ]]; then
    DOFNUM=7
elif [[ "$DOF" = "H3" ]]; then
    DOFNUM=8
elif [[ "$DOF" = "V1" ]]; then
    DOFNUM=9
elif [[ "$DOF" = "V2" ]]; then
    DOFNUM=10
elif [[ "$DOF" = "V3" ]]; then
    DOFNUM=11   
else
    echo '${DOF} is invalid.'
    exit 1;
fi

# Check Correct DOF
if [ "$DOF" = "P" ]; then
    if [ "$STAGE" = "IP" ]; then
	exit 1;
    fi
elif [ "$DOF" = "R" ]; then
    if [ "$STAGE" = "IP" ]; then
	exit 1;
    fi
elif [ "$DOF" = "V" ]; then
    if [ "$STAGE" = "IP" ]; then
	exit 1;
    fi
fi	

# Check BW
BW=$5
if [ "$STAGE" = "BF" ]; then
    if [ "$DOF" = "Y" ]; then    
	BW=0.001
    elif [ "$STAGE" = "IP" ]; then
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

# Check STATE
STATE=`caget -t K1:GRD-VIS_${SUS}_STATE_S` 
if [ $? -gt 0 ]; then
    exit # fixme
fi

# Check Template
templates_dir=/kagra/Dropbox/Measurements/VIS/scripts/automeasurement/templates
template=${templates_dir}/PLANT_${SUS}_STATE_${STAGE}_0000.xml
if [ ! -f $template ]; then
    echo 'No template file ${template}'
    exit 1;
fi

# Replacement for GAS filter
if [ $STAGE = GAS ]; then
    STAGE=$4
    DOF=$2
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

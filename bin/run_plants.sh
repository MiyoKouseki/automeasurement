#!/bin/bash
source /kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/settings
export EPICS_CA_ADDR_LIST=10.68.10.5
#
if [ $# -ne 4 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo "実行するには4個の引数が必要です。" 1>&2
  exit 1
fi

#
SUS=$1
STAGE=$2
EXC=$3
DOF=$4

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
    DOFS=(L T Y P R V F0 F1 F2 F3 BF H1 H2 H3 V1 V2 V3)
elif [ "$DOF" = "HOR" ]; then
    DOFS=(L T Y H1 H2 H3)
elif [ "$DOF" = "VER" ]; then
    DOFS=(P R V V1 V2 V3)
else
    DOFS=${DOF}
fi

# Confirmation
echo -e " \033[1;31mSupension : ${SUS}\033[0;39m"
echo -e " \033[1;31mStage     : ${STAGES[@]}\033[0;39m"
echo -e " \033[1;31mExcitation: ${EXC}\033[0;39m"
read -p "(y/n):" YN
if [ "${YN}" = "debug" ]; then
    DEBUG=0
    QUICK=0
elif [ "${YN}" = "quick" ]; then
    DEBUG=0
    QUICK=1        
elif [ "${YN}" = "y" ]; then
    DEBUG=1
    QUICK=0    
elif [ "${YN}" = "q" ]; then
    DEBUG=1    
    QUICK=1
else
    echo "you chose ${YN}. Stop. "
  exit 1;
fi

# Check if other workers measure the same suspension.
echo "OK. No one measure ${SUS}"

# Set Refnumber
refnum=`date +%Y%m%d%H%M`
get_grdstate(){
    SUS=$1
    STATE=`caget -t K1:GRD-VIS_${SUS}_STATE_S`
    if [ $? -gt 0 ]; then
	exit # fixme
    fi
    STATE=${STATE/_/}
    echo $STATE
}

get_exc_channel(){
    SUS=$1
    STAGE=$2
    EXC=$3
    DOF=$4
    if [ $STAGE = GAS ]; then
	STAGE=$4
	DOF=$2
    fi
    echo K1:VIS-${SUS}_${STAGE}_${EXC}_${DOF}_EXC    
}

get_template(){
    SUS=$1
    STAGE=$2
    template=${TEMPLATES_DIR}/PLANT_${SUS}_${STAGE}.xml
    if [ ! -f $template ]; then
	echo "No template file ${template}"
	exit 1;
    fi
    echo $template
}

get_output(){
    SUS=$1
    STATE=$2
    STAGE=$3
    EXC=$4
    DOF=$5
    refnum=$6
    # Check outputs_dir
    outputs_dir=${PLANTS_DIR}/${SUS}/`date +%Y/%m`
    if [ ! -e ${outputs_dir} ]; then
	mkdir -p ${outputs_dir}
    fi
    # Check output file
    output=${outputs_dir}/PLANT_${SUS}_${STATE}_${STAGE}_${EXC}_${DOF}_${refnum}.xml
    if [ -f $output ]; then
	echo '${output} already exists.'
	exit 1;
    fi
    echo $output
}

# Run

STATE=`get_grdstate $SUS`
echo $STATE
for STAGE in ${STAGES[@]}; do
    template=`get_template $SUS $STAGE`
    for DOF in ${DOFS[@]}; do       	
	output=`get_output $SUS $STATE $STAGE $EXC $DOF $refnum`
	exc_channel=`get_exc_channel ${SUS} ${STAGE} ${EXC} ${DOF}`
	run_plant.sh ${template} ${output} ${exc_channel} ${DEBUG} ${QUICK}	
    done
done

echo Done

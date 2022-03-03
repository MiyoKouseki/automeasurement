#!/bin/bash

source /kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/settings

num=$1

sus=`caget -t K1:ATM-VIS_ANS_${num}_SUS`
stg=`caget -t K1:ATM-VIS_ANS_${num}_STG`
sts=`caget -t K1:ATM-VIS_ANS_${num}_STS`
exc=`caget -t K1:ATM-VIS_ANS_${num}_EXC`
dofs=`caget -t K1:ATM-VIS_ANS_${num}_DOF`
ref=`caget -t K1:ATM-VIS_ANS_${num}_REF`

yyyy=${ref:0:4}
mm=${ref:4:2}

echo $dofs
read -p "Choose dofs:" dof
if [[ "$dofs" == *${dof}* ]]; then
    fname=${PLANTS_DIR}/${sus}/${yyyy}/${mm}/PLANT_${sus}_${sts}_${stg}_${exc}_${dof}_${ref}.xml
else
    echo "Error $dof"
    exit 1;
fi

if [ -f $fname ]; then  
    diaggui $fname
fi


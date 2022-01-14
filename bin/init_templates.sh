#!/bin/bash

prefix=/kagra/Dropbox/Measurements/VIS/scripts/automeasurement/templates

SUSPENSIONS=(ITMX ETMY ITMY BS SRM SR2 SR3 PRM PR2 PR3)
STAGES=(IP BF GAS MN IM)
for SUS in ${SUSPENSIONS[@]}; do
    for STG in ${STAGES[@]}; do    
	from=${prefix}/PLANT_ETMX_STATE_${STG}_0000.xml
	to=${prefix}/PLANT_${SUS}_STATE_${STG}_0000.xml
	cp ${from} ${to}
	sed -i -e "s/-ETMX_/-${SUS}_/" ${to}
    done
done    

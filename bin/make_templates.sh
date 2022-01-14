#!/bin/bash

prefix=/kagra/Dropbox/Measurements/VIS/scripts/automeasurement/templates


SUSPENSIONS=(ETMX ETMY ITMY)
STAGES=(IP BF GAS MN IM)
for SUS in ${SUSPENSIONS[@]}; do
    for STG in ${STAGES[@]}; do    
	from=${prefix}/PLANT_ITMX_STATE_${STG}_0000.xml
	to=${prefix}/PLANT_${SUS}_STATE_${STG}_0000.xml
	cp ${from} ${to}
	sed -i -e "s/-ITMX_/-${SUS}_/" ${to}
    done
done    

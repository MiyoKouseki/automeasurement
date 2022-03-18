#!/bin/bash

prefix_from=/kagra/Dropbox/Subsystems/VIS/Scripts/automeasurement/templates
prefix_to=/kagra/Dropbox/Measurements/VIS/TEMPLATES

#TYPEA
SUSPENSIONS=(ETMX ITMX ETMY ITMY)
STAGES=(IP BF GAS MN IM)
for SUS in ${SUSPENSIONS[@]}; do
    for STG in ${STAGES[@]}; do    
	from=${prefix_from}/PLANT_TYPEA_${STG}.xml
	to=${prefix_to}/PLANT_${SUS}_${STG}.xml
	cp ${from} ${to}
	sed -i -e "s/-ETMX_/-${SUS}_/" ${to}
    done
done    


#TYPEB
SUSPENSIONS=(SR2 SR3 SRM BS)
STAGES=(IP GAS IM TM)
for SUS in ${SUSPENSIONS[@]}; do
    for STG in ${STAGES[@]}; do    
	from=${prefix_from}/PLANT_TYPEB_${STG}.xml
	to=${prefix_to}/PLANT_${SUS}_${STG}.xml
	cp ${from} ${to}
	sed -i -e "s/-SR2_/-${SUS}_/" ${to}
    done
done    


# TYPEBP
SUSPENSIONS=(PR2 PR3 PRM)
STAGES=(BF GAS IM TM)
for SUS in ${SUSPENSIONS[@]}; do
    for STG in ${STAGES[@]}; do    
	from=${prefix_from}/PLANT_TYPEBP_${STG}.xml
	to=${prefix_to}/PLANT_${SUS}_${STG}.xml
	cp ${from} ${to}
	sed -i -e "s/-PR2_/-${SUS}_/" ${to}
    done
done    

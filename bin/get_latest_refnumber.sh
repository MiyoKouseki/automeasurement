#!/bin/bash
find /kagra/Dropbox/Measurements/VIS/PLANT/ -name '*xml' | sed -r "s/^.*_([0-9]{12})\.xml$/\1/g" | grep -v xml | sort -r | uniq | head -n1

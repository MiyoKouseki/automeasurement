#!/bin/bash

mkdir -p ../templates

rsync --delete -ave \
      ../templates/ \
      ssh k1ctr:/kagra/Dropbox/Measurements/VIS/TEMPLATES

#!/bin/bash

mkdir -p ../templates

rsync --delete -ave \
      ssh k1ctr:/kagra/Dropbox/Measurements/VIS/TEMPLATES/ \
      ../templates

#!/bin/bash
refnum=`date +%Y%m%d%H%M`
tar -czvf ./archive/$refnum.tgz ./*xml

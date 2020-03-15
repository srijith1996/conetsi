#!/bin/bash

# extract

mkdir -p node-data

idlist=$( awk '{print $2}' $1 | sort | uniq )

for id in $idlist; do 
  echo "extracting $id"
  grep $id $1 >> node-data/$id.log
done



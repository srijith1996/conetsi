#!/bin/bash

# rewrite the information in the NMS in the following form
# gen-id   #of hops    size   # of neighbors

hops=($( grep 'Number of hops' $1 | awk '{print $NF}' ))
sizes=($( grep 'Packet size' $1 | awk '{print $NF}' ))
genids=($( grep 'Number of Entries' $1 -B6 | grep 'Node' | awk '{print $NF}' ))
numneighs=()
topohops=()

for i in ${!genids[*]}; do
  numneighs[$i]=$( grep ${genids[$i]} $2 | awk -F"," '{print $(NF-1)}' )
  topohops[$i]=$( grep ${genids[$i]} $2 | awk -F"," '{print $NF}' )
done

for i in ${!hops[*]}; do #((i=0;i<${#hops[@]};++i)); do
  printf "%s, %s, %s, %s, %s\n" "${genids[$i]}" "${hops[$i]}" "${sizes[$i]}" "${topohops[$i]}" "${numneighs[$i]}"
done

#!/bin/bash
if [ $# -lt 2 ]; then
  echo "Usage: catalot.sh <prefix> <time_stamp>"
  echo "Available prefix: rho, rhoe, u, v, T, visc "
  exit 0
fi

pref=$1
num=$2
if [ $? -eq 0 ]; then
  cat ${pref}prof${num}p1 ${pref}prof${num}p0 ${pref}prof${num}p3 ${pref}prof${num}p2 > ${pref}prof${num}
#  echo "cattingg"
fi


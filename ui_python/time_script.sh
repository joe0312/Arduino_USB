#!/bin/bash

echo "Hello shell script"

read -p "Please input USB open time(s) : " opentime
read -p "Please input USB close time(s) : " closetime

while :
do
  python ui_python.py Y  
  sleep $closetime
  python ui_python.py N
  sleep $opentime
done

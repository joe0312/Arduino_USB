#!/bin/bash


while [ "$1" ]
do
       	case $1 in
	-m)
		if [ $2 -ge 0 -a $3 -ge 0 ];then
			opentime=$2
			closetime=$3
			shift 3
		else
			echo "time input error!!"
			echo "Please input : -m opentime closetime" 
                	exit 1
		fi
		;;
	-i|--interactive)
		read -p "Please input USB open time(s) : " opentime
		read -p "Please input USB close time(s) : " closetime
		shift
		;;
	-y|-Y|--on)
		opentime=1
                closetime=0
                shift
                ;;
	-n|-N|--off)
                opentime=0
                closetime=1
                shift 
                ;;
	*) 
		echo "input error!!" 
		exit 1 
		;;
	esac
done


if [ $opentime \> 0 -a $closetime \> 0 ];then
	while :
	do
		sleep $opentime
		python ui_python.py Y
		sleep $closetime
                python ui_python.py N
	done
elif [ $closetime \> 0 ];then
 	python ui_python.py N
elif [ $opentime \> 0 ];then
       	python ui_python.py Y
fi


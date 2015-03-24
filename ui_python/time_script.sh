#!/bin/sh

###### Default ######
if [ -z $1 ];then
	devopt="auto"
	read -p "Please input USB open time(s) : " opentime
        read -p "Please input USB close time(s) : " closetime
fi

###### Variables ####
while [ "$1" ]
do
	case $1 in
	-d|--dev)
		devopt=$2
		shift 2
		;;
	-t|--time)
		if [ $2 -ge 0 -a $3 -ge 0 ];then
			opentime=$2
			closetime=$3
			shift 3
		else
			echo "time input error!!"
			echo "Please input : -t opentime closetime"
                	exit 1
		fi
		;;
	-m|--mode)
		if [ $2 == "on" -o $2 == "Y" ];then
			opentime=1
			closetime=0
		elif [ $2 == "off" -o $2 == "N" ];then
			opentime=0
			closetime=1
		else
			echo "mode input error!!"
		fi
		shift 2
		;;
	*)
		echo "input format error!!"
		exit 1
		;;
	esac
done

##### Operating mode #####
if [ $opentime \> 0 -a $closetime \> 0 ];then
	while :
	do
		sleep $opentime
		python ui_python.py $devopt Y
		sleep $closetime
		python ui_python.py $devopt N
	done
elif [ $closetime \> 0 ];then
	python ui_python.py $devopt N
elif [ $opentime \> 0 ];then
	python ui_python.py $devopt Y
fi


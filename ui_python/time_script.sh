#!/bin/sh


###### Default ######
if [ $# -eq 0 ];then
	devopt="auto"
	op_mode="loop"
	read -p "Please input USB open time(s) : " opentime
        read -p "Please input USB close time(s) : " closetime
fi

###### Variables ####
variable=`getopt -o d:o:c:m: -l dev:,opentime:,closetime:,mode: -- "$@"`
eval set -- $variable

while [ "$1" ]
do
	case $1 in
	-d|--dev)
		devopt=$2
		shift 2
		;;
	-o|--opentime)
		if [ `echo $2 | grep "^[0-9]*$"` ];then
			op_mode="loop"
			opentime=$2
			shift 2
		else
			echo "time input error!!"
			echo "Please input : -o opentime"
                	exit 1
		fi
		;;
	-c|--closetime)
		if [ `echo $2 | grep "^[0-9]*$"` ];then
			op_mode="loop"
			closetime=$2
			shift 2
		else
			echo "time input error!!"
			echo "Please input : -c closetime"
			exit 1
		fi
		;;
	-m|--mode)
		if [ $2 = "on" -o $2 = "Y" ];then
			op_mode="single"
			switchopt="Y"
		elif [ $2 = "off" -o $2 = "N" ];then
			op_mode="single"
			switchopt="N"
		else
			echo "mode input error!!"
			exit 1
		fi
		shift 2
		;;
	--)
		shift
		break
		;;
	*)
		echo "input format error!!"
		exit 1
		;;
	esac
done

##### Operating mode #####
if [ "$op_mode" = "loop" ];then
	while :
	do
		sleep $opentime
		python ui_python.py $devopt Y
		sleep $closetime
		python ui_python.py $devopt N
	done
elif [ "$op_mode" = "single" ];then
	python ui_python.py $devopt $switchopt
fi


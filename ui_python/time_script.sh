#!/bin/sh


###### Default ######
opentime=0
closetime=0

###### Interactive ######
if [ $# -eq 0 ];then
	read -p "Please input USB open time(s) : " opentime
        read -p "Please input USB close time(s) : " closetime
	echo `python ui_python.py auto D`
        read -p "Please input Device com port : " devopt
fi

###### Variables ####
variable=`getopt -o d:o:c:m: -l dev:,opentime:,closetime:,mode: -- "$@"`
eval set -- $variable

while [ "$1" ]
do
	case $1 in
	-d|--dev)
		if [ $2 = "auto" ];then
			devoptstr=`python ui_python.py auto D`
			devopt=`echo $devoptstr | cut -d ' ' -f 5`
		else
			devopt=$2
		fi
		shift 2
		;;
	-o|--opentime)
		if [ `echo $2 | grep "^[0-9]*$"` ];then
			mode="time"
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
			mode="time"
			closetime=$2
			shift 2
		else
			echo "time input error!!"
			echo "Please input : -c closetime"
			exit 1
		fi
		;;
	-m|--mode)
		if [ $mode = "time" ];then
			echo "input format error(-m and -o/-c can't exist at the same time)!!"
			exit 1
		elif [ $2 = "on" -o $2 = "Y" ];then
			opemtime=1
		elif [ $2 = "off" -o $2 = "N" ];then
			closetime=1
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
if [ $opentime -gt 0 -a $closetime -gt 0 ];then
	while :
	do
		sleep $opentime
		python ui_python.py $devopt Y
		sleep $closetime
		python ui_python.py $devopt N
	done
elif [ $opentime -gt 0 ];then
	python ui_python.py $devopt Y
elif [ $closetime -gt 0 ];then
	python ui_python.py $devopt N
else
	echo "input format error!!"
fi


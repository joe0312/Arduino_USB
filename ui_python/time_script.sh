#!/bin/sh


RED=`echo "\33[31m"`
BLUE=`echo "\33[34m"`
WHITE=`echo "\33[37m"`

###### Usage here documents ######
usage_heredoc(){
cat << EOF

${BLUE}NAME${WHITE}
	time_script - USB connect mode

${BLUE}SYNOPSIS${WHITE}
	time_script [${BLUE}options${WHITE}]
	time_script
	time_script ${BLUE}-d ${RED}deviceopt${WHITE} ${BLUE}-t ${RED}opentime,closetime${WHITE}
	time_script ${BLUE}-d ${RED}deviceopt${WHITE} ${BLUE}-s ${RED}switchopt${WHITE}

${BLUE}DESCRIPTION
	${BLUE}-d,--device ${RED}deviceopt${WHITE}
		Connect to controller(Arduino) with device com port(${RED}deviceopt${WHITE})
		If you don't know the corresponding com port,you can use ${RED}"auto"${WHITE} to detect the device

	${BLUE}-t,--time ${RED}opentime,closetime${WHITE}
		Use time loop mode to control USB connection
		Repeat connect ${RED}"opentime(s)"${WHITE} and disconnect ${RED}"closetime(s)"${WHITE} action

	${BLUE}-s,--switch ${RED}switchopt${WHITE}
		Use simple switch mode to control USB connection
		Connect USB when switchopt is ${RED}"on"${WHITE} or ${RED}"Y"${WHITE}
		Disconnect USB when switchopt is ${RED}"off"${WHITE} or ${RED}"N"${WHITE}

EOF
}


###### Check device com port ######
check_ui_python(){
	devoptmsg=`python ui_python.py $1 $2`
	echo $devoptmsg
	if [ `echo $devoptmsg | cut -d ' ' -f 1` = "Error:" ];then
		exit 1
	fi
}

###### Interactive mode ######
if [ $# -eq 0 ];then
	read -p "Please input USB open time(s) : " opentime
	read -p "Please input USB close time(s) : " closetime
	if [ $opentime -eq 0 ] && [ $closetime -eq 0 ];then
		echo "Error: invalid time input"
		exit 1
	elif [ $closetime -eq 0 ];then
		op_mode="switch"
		switchopt="Y"
	elif [ $opentime -eq 0 ];then
		op_mode="switch"
		switchopt="N"
	else
		op_mode="time"
	fi

	echo `python ui_python.py auto scan`
	read -p "Please input Device com port : " devopt
	check_ui_python $devopt scan
fi


###### Variables analysis ######
variable=`getopt -o d:t:s:h -l device:,time:,switch:,help -- "$@"`
eval set -- "$variable"

while [ "$1" ]
do
	case $1 in
	-d|--device)
		check_ui_python $2 scan
		if [ $2 = "auto" ];then
			devopt=`echo $devoptmsg | cut -d ' ' -f 5`
		else
			devopt=$2
		fi
		shift 2
		;;
	-t|--time)
		if [ `echo $2 | cut -d "," -f 1 | grep "^[0-9]*$"` ] && [ `echo $2 | cut -d "," -f 2 | grep "^[0-9]*$"` ];then
			opentime=`echo $2 | cut -d "," -f 1`
			closetime=`echo $2 | cut -d "," -f 2`
			if [ $opentime -eq 0 ] && [ $closetime -eq 0 ];then
				echo "Error: invalid time input"
				exit 1
			elif [ $closetime -eq 0 ];then
				op_mode="switch"
				switchopt="Y"
			elif [ $opentime -eq 0 ];then
				op_mode="switch"
				switchopt="N"
			else
				op_mode="time"
			fi
			shift 2
		else
			echo "Error: invalid time input"
			echo "Please input : -t opentime(s),closetime(s)"
			exit 1
		fi
		;;
	-s|--switch)
		if [ $2 = "on" -o $2 = "Y" ];then
			op_mode="switch"
			switchopt="Y"
		elif [ $2 = "off" -o $2 = "N" ];then
			op_mode="switch"
			switchopt="N"
		else
			echo "Error: invalid switch choose"
			echo "Please input : -s on(Y)\off(N)"
			exit 1
		fi
		shift 2
		;;
	-h|--help)
		usage_heredoc
		exit 1
		;;
	--)
		shift
		break
		;;
	*)
		echo "Error: illegal input parameter format"
		exit 1
		;;
	esac
done


##### Analysis mode and operating #####
if [ ! $op_mode ];then
	echo "Error: input parameter not enough"
	echo "Please input : -s on(Y)\off(N) or -t opentime(s),closetime(s)"
elif [ $op_mode = "time" ];then
	while :
	do
		sleep $opentime
		check_ui_python $devopt Y
		sleep $closetime
		check_ui_python $devopt N
	done
elif [ $op_mode = "switch" ];then
	check_ui_python $devopt $switchopt
fi


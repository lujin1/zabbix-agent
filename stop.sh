#! /bin/sh
pid=/var/run/zabbix/zabbix_agentd.pid
#kill $pid
if [ -e "$pid" ]
then
opid=`cat $pid`
echo "stoping zabbix pid:$opid"
echo "........................"
kill $opid
sleep 1
echo "stoped zabbix pid:$opid"
else 
echo "zabbix 已经停止，请检查进程"
fi



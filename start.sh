#! /bin/sh
pid=/var/run/zabbix/zabbix_agentd.pid
if [ -e "$pid" ]
then 
echo "zabbix not stoped 请检查进程"
else
/usr/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agentd.conf
sleep 1
echo "zabbix started"
fi

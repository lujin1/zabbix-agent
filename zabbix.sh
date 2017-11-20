#! /bin/sh
### 2017-10-09 
### by lujin
### 安装agent


echo “安装zabbix_agent rpm”
rpm -ivh zabbix-agent-3.2.3-1.el7.x86_64.rpm
rm -rf /etc/zabbix/zabbix_agentd.conf
cp zabbix_agentd.conf /etc/zabbix/zabbix_agentd.conf
cp *.sh /etc/zabbix/
chmod 770 /etc/zabbix/*.sh
echo “start zabbix_agent”
sh /etc/zabbix/start.sh
echo "ps -ef|grep zabbix"
ps -ef|grep zabbix




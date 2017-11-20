# !/usr/bin/python
# coding:utf-8
# 后台一键部署zabbix agent和添加主机（仅限监控linux）
# by lujin
# 2017-11-16
import json
import urllib2
from urllib2 import URLError
import sys,os,socket

class zabbix_api:
    def __init__(self):
        self.url = '10.171/api_jsonrpc.php' #修改URL
        self.header = {"Content-Type":"application/json"}
    def user_login(self):
        data = json.dumps({
	                       "jsonrpc": "2.0",
	                       "method": "user.login",
	                       "params": {
	                                  "user": "Admin", #修改用户名
	                                  "password": "" #修改密码
	                                  },
	                       "id": 0
	                       })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print 'url error for zabbix ', e
            sys.exit()
        try:
            response = json.loads(result.read())
            result.close()
            self.authID = response['result']
            return self.authID
        except KeyError:
            print 'user or password error!'
            sys.exit()
    def host_get(self,hostName=''):
        data=json.dumps({
	            "jsonrpc": "2.0",
	            "method": "host.get",
	            "params": {
	                      "output": "extend",
	                      "filter":{"host":hostName}
	                      },
	            "auth": self.user_login(),
	            "id": 1
	            })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
         #   print ("主机数量: %s"%(len(response['result'])))
            for host in response['result']:
                status = {"0":"OK","1":"Disabled"}
             #   available = {"0":"Unknown","1":"available","2":"Unavailable"}
            #print host
            if len(hostName)==0:
                print ("HostID : %s HostName : %s Status :%s"%(host['hostid'],host['name'],status[host['status']]))
            else:
                print ("HostID : %s HostName : %s Status :%s"%(host['hostid'],host['name'],status[host['status']]))
                return host['hostid']
        except UnboundLocalError:
            print '主机未添加!'
    def hostgroup_get(self, hostgroupName=''):
        data = json.dumps({
                    "jsonrpc":"2.0",
                            "method":"hostgroup.get",
	                       "params":{
	                                 "output": "extend",
	                                 "filter": {
	                                            "name": hostgroupName
	                                            }
	                                 },
	                       "auth":self.user_login(),
	                       "id":1,
	                       })
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
            for group in response['result']:
                if len(hostgroupName) == 0:
                    print (u"主机组: %s" % (group['name']))
                else:
                    print (u"主机组: %s" % (group['name']))
                    self.hostgroupID = group['groupid']
                    return group['groupid']

    def template_get(self,templateName=''):
        data = json.dumps({
	                       "jsonrpc":"2.0",
	                       "method": "template.get",
	                       "params": {
	                                  "output": "extend",
	                                  "filter": {
	                                             "name":templateName
	                                             }
	                                  },
	                       "auth":self.user_login(),
	                       "id":1,
	                       })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
           # print response
            for template in response['result']:
                if len(templateName)==0:
                    print ("template: %s  id: %s" % (template['name'], template['templateid']))
                else:
                    self.templateID = response['result'][0]['templateid']
                    print u"模板 : %s" %templateName
                    return response['result'][0]['templateid']

    def hostgroup_create(self,hostgroupName):
        if self.hostgroup_get(hostgroupName):
            print ("hostgroup  %s is exist !" %hostgroupName)
            sys.exit()
        data = json.dumps({
	                      "jsonrpc": "2.0",
	                      "method": "hostgroup.create",
	                      "params": {
	                      "name": hostgroupName
	                      },
	                      "auth": self.user_login(),
	                      "id": 1
	                      })
        request=urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
            print ("添加主机组: %s  hostgroupID: %s" % (hostgroupName, response['result']['groupids']))

    def host_create(self, hostip,hostgroupName, templateName):
        # if self.host_get(hostip):
        #     print ("该主机已经添加!")
        #     sys.exit()
        group_list = []
        template_list = []
        var1 = {}
        var2 = {}
        var1['groupid'] = self.hostgroup_get(hostgroupName)
        var2['templateid'] = self.template_get(templateName)
        group_list.append(var1)
        template_list.append(var2)
        # for i in hostgroupName.split(','):
        #     var = {}
        #     var['groupid'] = self.hostgroup_get(i)
        #     group_list.append(var)
        # for i in templateName.split(','):
        #     var={}
        #     var['templateid']=self.template_get(i)
        #     template_list.append(var)
        data = json.dumps({
	                        "jsonrpc":"2.0",
	                        "method":"host.create",
	                        "params":{
	                                 "host": hostip,
	                                 "interfaces": [
	                                 {
	                                 "type": 1,
	                                 "main": 1,
	                                 "useip": 1,
	                                 "ip": hostip,
	                                 "dns": "",
	                                 "port": "10050"
	                                  }
	                                 ],
	                               "groups": group_list,
	                               "templates": template_list,
	                                 },
	                        "auth": self.user_login(),
	                        "id":1
	    })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
            result = urllib2.urlopen(request)
            response = json.loads(result.read())
            result.close()
            print ("添加主机 : %s  tid :%s" % (hostip, response['result']['hostids']))


if __name__ == "__main__":
    zabbix = zabbix_api()
    commands.getoutput(sh zabbix.sh) # 安装agent
    hostip = socket.gethostbyname(socket.gethostname()) #获取本地ip地址
    groups_key = python groups_api.py %s %(hostip)
    groups_key_D = groups_key.upper() #转为大写
    if groups_key_D == 'HRP':
        hostgroup = "2HRP事业部"
    elif groups_key_D == 'HR':
        hostgroup = "4招聘"
    elif groups_key_D == 'YLY':
        hostgroup = "1医疗云事业部"
    elif groups_key_D == 'FEIYI':
        hostgroup = "3飞医事业部"
    elif groups_key_D == 'YDYL':
        hostgroup = "6移动医疗事业部"
    else:
        hostgroup = "Linux servers"
    template = 'Template OS Linux'
    host = zabbix.host_get(hostip)
    group = zabbix.hostgroup_get(hostgroup)
    tem = zabbix.template_get(template)
    #zabbix.hostgroup_get()
    if host is None:
        if tem is None:
            print '该模板不存在，请检查！'
            print 'exit......'
            sys.exit()
        else:
            if group is None:
                print '%s 该主机组不存在！' %(hostgroup)
                print '正在添加主机组 %s......' %(hostgroup)
                zabbix.hostgroup_create(hostgroup)
                print '正在添加主机 %s......' % (hostip)
                zabbix.host_create(hostip,hostgroup,template)
            else:
                print '正在添加主机 %s......' % (hostip)
                zabbix.host_create(hostip, hostgroup, template)
    else:
        print '该主机已经添加！'
        print 'exit......'
        sys.exit()
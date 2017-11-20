#!/usr/bin/python
#coding=utf-8
# by lujin 卢进
# 2017-11-20
# 获取实例名称
# 需要安装阿里云sdk
# pip install aliyun-python-sdk-ecs
# pip install aliyun-python-sdk-slb

import sys,json,time
from aliyunsdkcore import client
from aliyunsdkslb.request.v20140515 import  DescribeLoadBalancersRequest
from aliyunsdkslb.request.v20140515 import SetBackendServersRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
import json

ID = ''
Secret = ''
RegionId = 'cn-beijing'



#后端服务器ip
Ip = sys.argv[1]
InsIp = [Ip]

#连接阿里云平台
clt = client.AcsClient(ID,Secret,RegionId)


def GetInstancesId(InsIp):

    try:
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')

        request.add_query_param('RegionId', RegionId)
        request.add_query_param('InnerIpAddresses', InsIp)
        response = clt.do_action_with_exception(request)
	#print response
        nobuer = response.replace('false','0').replace('true','1')
		dictecs = eval(nobuer)
		groups_key = dictecs['Instances']['Instance'][0]['InstanceName'].split('-',1)[0]        
        return groups_key

    except:
        request = DescribeInstancesRequest.DescribeInstancesRequest()
        request.set_accept_format('json')
        request.add_query_param('RegionId', RegionId)
        request.add_query_param('PrivateIpAddresses', InsIp)
        response = clt.do_action_with_exception(request)
        nobuer = response.replace('false','0').replace('true','1')
        dictecs = eval(nobuer)
		groups_key = dictecs['Instances']['Instance'][0]['InstanceName'].split('-',1)[0]
        return groups_key

groups_key = GetInstancesId(InsIp)
return groups_key

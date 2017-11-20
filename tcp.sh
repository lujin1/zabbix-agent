#! /bin/sh
netstat -an|grep $1|awk '/^tcp/{++S[$NF]}END{for(a in S) print S[a]}'


#!/usr/bin/env python

import requests
from requests_kerberos import HTTPKerberosAuth
import sys
import subprocess

top=True
data=[]
for i in subprocess.check_output(['/usr/sbin/repquota', '-O', 'csv', '-c', '/home']).splitlines():
    if top:
       top=False
       continue
    line=i.split(',')
    if line[0]=='root':
       continue
    username=line[0]
    used=line[3]
    quota=line[4]
    data.append({ 'username': username, 'used': used, 'quota': quota})
    if(len(data)>1000):
        response = requests.post('http://eniac.dcti.sut.ru/selfreg/process/quota',auth=HTTPKerberosAuth(), json = data)
        if response.status_code != 200:
            print(response.json())
        data=[]


response = requests.post('http://eniac.dcti.sut.ru/selfreg/process/quota',auth=HTTPKerberosAuth(), json = data)
if response.status_code != 200:
    print(response.json())

#!/usr/bin/env python3

import time
import subprocess
import requests
from requests_kerberos import HTTPKerberosAuth, DISABLED, OPTIONAL, REQUIRED

top=True
data=[]

def send_data(session, url, data):
    response = session.post(url, auth=HTTPKerberosAuth(mutual_authentication=REQUIRED), json = data)
    return response.status_code

def send_data_with_retry(session, url, data, retries):
    counter = 0
    code = 401
    while (code == 401) and (counter < retries):
        if counter > 0:
            print(counter)
        code = send_data(session, url, data)
        counter = counter + 1
        time.sleep(0.1)
    if counter >= retries:
        return False
    return True

s= requests.Session()
for i in subprocess.check_output(['/usr/sbin/repquota', '-O', 'csv', '-c', '/home']).splitlines():
    if top:
        top=False
        continue
    t=i.decode('utf-8')
    line=t.split(',')
    if line[0]=='root':
        continue
    username=line[0]
    used=line[3]
    quota=line[4]
    data.append({ 'username': username, 'used': used, 'quota': quota})
    if len(data)>1000:
        send_data_with_retry(s, 'http://srv-1.dcti.sut.ru/selfreg/process/quota', data, 50)
        data=[]


send_data_with_retry(s, 'http://srv-1.dcti.sut.ru/selfreg/process/quota', data, 50)

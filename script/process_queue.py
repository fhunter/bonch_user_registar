#!/usr/bin/env python3
import os
import subprocess
import sys

if "REMOTE_ADDR" in os.environ:
    print("Content/type: text/html")
    print("")
    print("Wrong page")
    exit(0)

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from my_db import Session, Queue

#This is not a CGI
s = Session()
queue = s.query(Queue).filter(Queue.done == 0).order_by(Queue.date.asc()).all()
for i in queue:
    username = i.username.username
    password = i.password
    commandline=f"""kadmin -p automator1/admin -k -t /etc/krb5.keytab -q "change_password -pw {password} {username}" """
    try:
        retcode = subprocess.call(commandline, shell=True)
        if retcode < 0:
            print(f"Child was terminated by signal {-retcode}", file=sys.stderr)
        else:
            if retcode == 0:
                i.done = True
            else:
                print(f"Child returned {retcode}", file=sys.stderr)
    except OSError as e:
        print(f"Execution failed: {e}", file=sys.stderr)

    commandline=f"""kadmin -p automator1/admin -k -t /etc/krb5.keytab -q "modprinc +needchange {username}" """ 
    try:
        retcode = subprocess.call(commandline, shell=True)
    except OSError as e:
        print(f"Execution failed: {e}", file=sys.stderr)
s.commit()

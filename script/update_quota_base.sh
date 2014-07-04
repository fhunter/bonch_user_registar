#!/bin/sh
#CREATE TABLE 'quota' (id primary key unique not null, username text not null unique, usedspace integer not null, softlimit integer not null);
echo "BEGIN TRANSACTION;"
/usr/sbin/repquota -c /home|awk '{if((sum >=5)&&($1!="")) { print "insert or replace into quota (username,usedspace,softlimit) values (\""$1"\","$3","$4");"};sum=sum+1;}'
echo "END TRANSACTION;"


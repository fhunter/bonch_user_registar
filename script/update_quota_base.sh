#!/bin/sh
#CREATE TABLE 'quota' (id primary key unique not null, username text not null unique, usedspace integer not null, softlimit integer not null);
/usr/sbin/repquota -c /home|awk '{if((sum >=5)&&($1!="")) { print "replace into quota ('username','usedspace','softlimit') values (\""$1"\","$3","$4");"};sum=sum+1;}'|mysql -u selfreg --password=nthininteasevencewor selfreg


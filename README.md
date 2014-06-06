# Утилита для сброса паролей и просмотра информации о пользователях

Для включения в Apache:

```
<Directory /var/www/selfreg>
    AddHandler cgi-script .cgi
    AddHandler cgi-script .py
    Options +ExecCGI
    AuthType Kerberos
    AuthName "Self registration admin zone"
    Krb5Keytab /etc/apache2/krb5.keytab
    KrbAuthRealm DCTI.SUT.RU
    KrbMethodNegotiate on
    KrbDelegateBasic on
    KrbMethodK5Passwd on
    KrbSaveCredentials on
    AuthzUnixgroup on
    Require group personal
    Require group teachers
</Directory>
```

Использованные модули:
 * modauth_kerberos
 * modauthz_unixgroup

Quota collection script:

```
#!/bin/sh
#CREATE TABLE 'quota' (id primary key unique not null, username text not null unique, usedspace integer not null, softlimit integer not null);
echo "BEGIN TRANSACTION;"
repquota -c /home|awk '{if((sum >=5)&&($1!="")) { print "insert or replace into quota (username,usedspace,softlimit) values (\""$1"\","$3","$4");"};sum=sum+1;}'
echo "END TRANSACTION;"
```

Crontab entry:

```
*/5 *  *   *   *     (/usr/local/sbin/update_quota_base.sh|su - www-data -c "sqlite3 /var/www/selfreg/database.sqlite3")        #update quota db
```

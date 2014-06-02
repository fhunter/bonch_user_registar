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

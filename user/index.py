#!/usr/bin/env python
import os
import cgi
import cgitb
cgitb.enable()

print "Content: text/html"
print ""
print "<pre>"
print os.environ["REMOTE_USER"]
print "</pre>"

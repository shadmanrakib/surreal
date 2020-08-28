#!/usr/bin/env python3
print ("Content-type: text/html\n")
import cgi

form = cgi.FieldStorage()
if 'sid' in form:
    sid = form.getvalue('sid')
    print(sid)
else:
    print('BAD')
    

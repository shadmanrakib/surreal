#!/usr/bin/env python3
print ("Content-type: text/html\n")

import hashlib, string, secrets, time, pickle, cgi, cgitb
import os.path
from os import path

data_dir = ''
cgitb.enable()

form = cgi.FieldStorage()

class Session:
    sids = []
    def __init__(self, username, ip, browser, ip_salt):
        self.username = username
        self.start_time = time.time()
        self.ip = ip
        self.ip_salt = ip_salt
        self.browser = browser
        choices = string.ascii_lowercase + string.ascii_uppercase + string.digits
        self.sid = ''
        for i in range(100):
            self.sid += secrets.choice(choices)
        while True:
            if not self.sid in sids:
                break
            self.sid = ''
            for i in range(100):
                print(self.sid)
                self.sid += secrets.choice(choices)
        sids.append(self.sid)
    def end(self):
        sids.remove(self.sid)
        sessions.pop(self.sid)
        
if path.exists(data_dir + "user.p"):
    user = pickle.load( open( data_dir + "user.p", "rb" ) )
else:
    user = {}
    pickle.dump(user, open( data_dir + "user.p", "wb" ) )

if path.exists("sessions.p"):
    sessions = pickle.load( open( data_dir + "sessions.p", "rb" ) )
    sids = list(sessions.keys())
else:
    sessions = {}
    sids = []
    pickle.dump(sessions, open( data_dir + "sessions.p", "wb" ) )

redirect = '''<html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="3; url = index.html" />
        <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=Open+Sans&family=Roboto&display=swap" rel="stylesheet">
        <link rel = "stylesheet" type = "text/css" href = "surrealUser.css" />
        <title></title>
      </head>
      <body>{0}</body>
    </html>'''

if 'sid' in form:
    sid = form.getvalue('sid')
    if sid in list(sessions.keys()):
        sessions[sid].end()
        pickle.dump(sessions, open( data_dir + "sessions.p", "wb" ) )
    redirect = '''<html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content="1; url = index.html" />
        <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=Open+Sans&family=Roboto&display=swap" rel="stylesheet">
        <link rel = "stylesheet" type = "text/css" href = "surrealUser.css" />
        <title></title>
      </head>
      <body>{}</body>
    </html>'''.format('Session Removed')

else:
    redirect = '''<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url = index.html" />
    <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=Open+Sans&family=Roboto&display=swap" rel="stylesheet">
    <link rel = "stylesheet" type = "text/css" href = "surrealUser.css" />
    <title></title>
  </head>
  <body></body>
</html>'''
    
print(redirect)
    

    

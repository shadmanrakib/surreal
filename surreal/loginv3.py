#!/usr/bin/env python3
print ("Content-type: text/html\n")

import hashlib, string, time, pickle, cgi, secrets, os, html
from os import path
import cgitb

cgitb.enable()

data_dir = ''

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

def get_data(s):
        r = s.split('\n')
        seprows = []
        for i in range(len(r) - 2):
            seprows.append(r[i + 1].split(','))
        return seprows
    
if path.exists(data_dir + "user.p"):
    user = pickle.load( open( data_dir + "user.p", "rb" ) )
else:
    user = {}
    pickle.dump(user, open( data_dir + "user.p", "wb" ) )
    

if path.exists(data_dir + "sessions.p"):
    sessions = pickle.load( open( data_dir + "sessions.p", "rb" ) )
    sids = list(sessions.keys())
    
else:
    sessions = {}
    sids = []
    pickle.dump(sessions, open( data_dir + "sessions.p", "wb" ) )

def generate_salt():
    salt = ''
    choices = string.printable
    for i in range(100):
        salt += secrets.choice(choices)
    return salt

form = cgi.FieldStorage()
if 'username' in form and 'password' in form:
    username = form.getvalue('username')
    password = form.getvalue('password')

    if username in list(user.keys()):
        pre_hpw, pre_salt = user[username]
        if pre_hpw == hashlib.pbkdf2_hmac('sha256', password.encode(), pre_salt.encode(), 100000).hex():
            salt = generate_salt()
            hashed_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
            user[username] = (hashed_pw, salt)
            for s in sids:
                if sessions[s].username == username:
                    sessions[s].end()
            ip_salt = generate_salt()
            ip = html.escape(os.environ["REMOTE_ADDR"])
            hashed_ip = hashlib.pbkdf2_hmac('sha256', ip.encode(), ip_salt.encode(), 100000).hex()
            session = Session(username, hashed_ip, html.escape(os.environ["HTTP_USER_AGENT"]), ip_salt)
            sessions[session.sid] = session
            pickle.dump(sessions, open( data_dir + "sessions.p", "wb" ) )
            pickle.dump(user, open( data_dir + "user.p", "wb" ) )
            response = (2, session.sid)
        else:
            response = (1, '<div class="message">Username and Password Do Not Match or Are Unknown</div>')
    else:
        response = (1, '<div class="message">Username and Password Do Not Match or Are Unknown</div>')
            
    #login(username, password)
else:
    response = (0, '''<form class="" action=loginv3.py method="post">
          <div class="form-title">
            LOGIN
          </div>
          <br>
          <label for="name">USERNAME </label>
          <br>
          <input type="text" name="username" id="username">
          <br>
          <label for="password">PASSWORD </label>
          <br>
          <input type="password" name="password" id="password">
          <br>
          <input type="submit" value="SUBMIT">
        </form>''')

if response[0] == 0:
    html = '''<!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=Open+Sans&family=Roboto&display=swap" rel="stylesheet">
        <link rel = "stylesheet" type = "text/css" href = "surrealUser.css" />
        <title></title>
      </head>
      <body>
        <div class="bg">
          <div class="container">
            <div class="logo">
              SURREAL
            </div>'''
    html += response[1]
    html += '''<div class="alternate-form">
          Do not have an account? <a href="registerv3.py">Register Here</a>
        </div>
      </div>
    </div>
  </body>
</html>
'''
if response[0] == 1:
    html = '''<!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=Open+Sans&family=Roboto&display=swap" rel="stylesheet">
        <link rel = "stylesheet" type = "text/css" href = "surrealUser.css" />
        <title></title>
      </head>
      <body>
        <div class="bg">
          '''
    html += response[1]
    html += '''
          <div class="container">
            <div class="logo">
              SURREAL
            </div>
            <form class="" action=loginv3.py method="post">
              <div class="form-title">
                LOGIN
              </div>
              <br>
              <label for="name">USERNAME </label>
              <br>
              <input type="text" name="username" id="username">
              <br>
              <label for="password">PASSWORD </label>
              <br>
              <input type="password" name="password" id="password">
              <br>
              <input type="submit" value="SUBMIT">
            </form><div class="alternate-form">
          Do not have an account? <a href="registerv3.py">Register Here</a>
        </div>
      </div>
    </div>
  </body>
</html>
'''
if response[0] == 2:
    html = '''<!DOCTYPE html>
    <html lang="en" dir="ltr">
      <head>
        <meta charset="utf-8">
        <link href="https://fonts.googleapis.com/css2?family=Libre+Baskerville&family=Open+Sans&family=Roboto&display=swap" rel="stylesheet">
        <link rel = "stylesheet" type = "text/css" href = "surrealUser.css" />
        <title></title>
      </head>
      <body onload="document.forms['sidform'].submit()">
        <div class="bg">
          '''
    html += '<div class="message">Logged in. Redirecting.</div>'
    html += '''
          <div class="container">
            <div class="logo">
              SURREAL
            </div>
            <form id="sidform" name="sidform" action=home.py method="post">'''
    html += '<input type="hidden" id="sid" name="sid" value="' + response[1] + '">'
    html += '''
            </form>
      </div>
    </div>
  </body>
</html>
'''
print(html)
  

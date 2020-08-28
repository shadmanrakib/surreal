#!/usr/bin/env python3
print ("Content-type: text/html\n")

import hashlib, string, time, pickle, cgi, secrets
import os.path
from os import path

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
            
    if not (username == 'user' or username == 'sessions'):
        if not username in list(user.keys()):
            if any(not i.isalnum() for i in password) and any(i.isdigit() for i in password) and any(i.isalpha() for i in password) and any(i.isupper() for i in password) and any(i.islower() for i in password) and (len(password) >= 16):
                salt = generate_salt()
                hashed_pw = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
                user[username] = (hashed_pw, salt)
                pickle.dump(user, open( data_dir + "user.p", "wb" ) )
                response = (2, '<div class="message">Successfully Registered. You will be redirected in 3 seconds.</div>')
            else:
                response = (1, '<div class="message">Password does not meet the criteria</div>')
        else:
            response = (1, '<div class="message">Username is already in use</div>')
    else:
        response = (1, '<div class="message">Username not permitted</div>')

    #register(username, password)
else:
    response = (0, '''<form class="" action=registerv3.py method="post">
          <div class="form-title">
            REGISTER
          </div>
          <br>
          <label for="name">USERNAME </label>
          <br>
          <input type="text" name="username" id="username">
          <br>
          <label for="password">PASSWORD </label>
          <br>
          <div class="tooltip">
            <input type="password" name="password" id="password">
            <span class="tooltiptext">
              Valid passwords must meet the following criteria:
              <ul>
                <li>Contain at least 16 characters</li>
                <li>Contain at least one uppercase letter</li>
                <li>Contain at least one lowercase letter</li>
                <li>Contain at least one digit</li>
                <li>Contain at least one special character (eg. !, @, #, $, %, ^, and *)</li>
              </ul>
            </span>
          </div>
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
              Already have an account? <a href="loginv3.py">Login Here</a>
            </div>
          </div>
        </div>
      </body>
    </html>'''
elif response[0] == 1:
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
            <form class="" action=registerv3.py method="post">
              <div class="form-title">
                REGISTER
              </div>
              <br>
              <label for="name">USERNAME </label>
              <br>
              <input type="text" name="username" id="username">
              <br>
              <label for="password">PASSWORD </label>
              <br>
              <div class="tooltip">
                <input type="password" name="password" id="password">
                <span class="tooltiptext">
                  Valid passwords must meet the following criteria:
                  <ul>
                    <li>Contain at least 16 characters</li>
                    <li>Contain at least one uppercase letter</li>
                    <li>Contain at least one lowercase letter</li>
                    <li>Contain at least one digit</li>
                    <li>Contain at least one special character (eg. !, @, #, $, %, ^, and *)</li>
                  </ul>
                </span>
              </div>
              <br>
              <input type="submit" value="SUBMIT">
            </form>'''
    html += '''<div class="alternate-form">
              Already have an account? <a href="loginv3.py">Login Here</a>
            </div>
          </div>
        </div>
      </body>
    </html>'''
elif response[0] == 2:
    html = '''<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url = index.html" />
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
        <form class="">
          <div class="form-title">
            REGISTER
          </div>
          <br>
          <label for="name">USERNAME </label>
          <br>
          <input type="text" name="username" id="username">
          <br>
          <label for="password">PASSWORD </label>
          <br>
          <div class="tooltip">
            <input type="password" name="password" id="password">
            <span class="tooltiptext">
              Valid passwords must meet the following criteria:
              <ul>
                <li>Contain at least 16 characters</li>
                <li>Contain at least one uppercase letter</li>
                <li>Contain at least one lowercase letter</li>
                <li>Contain at least one digit</li>
                <li>Contain at least one special character (eg. !, @, #, $, %, ^, and *)</li>
              </ul>
            </span>
          </div>
          <br>
          <input type="submit" value="SUBMIT">
        </form>
        <div class="alternate-form">
          Already have an account? <a href="loginv2.py">Login Here</a>
        </div>
      </div>
    </div>
  </body>
</html>
'''
    
print(html)

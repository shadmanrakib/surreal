#!/usr/bin/python
import cgi, cgitb, pickle
import os.path as path
print("Content-type: text/html\n")

cgitb.enable()

inpts = cgi.FieldStorage()

data_dir = ''

def cartTotal(username):
        total = 0.00
        for item in carts[username]:
            total += float(item.price)
        return "%.2f" % total
    
def fill_class(html, cls, content):
    cls_pos = html.find('class=' + '"{cls}"'.format(cls=cls))
    if cls_pos != -1:
        content_start = cls_pos + html[cls_pos + 1:].find('>') + 2
        html = html[:content_start] + content + html[content_start:]
        return html
    
class Item():
    def __init__(self, username, pic, name, price, status, seller):
        self.username = username
        self.pic = pic
        self.name = name
        self.price = price
        self.status = status
        self.seller = seller
    def remove(self):
        carts[self.username].remove(self)

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

if path.exists(data_dir + "carts.p"):
    carts = pickle.load( open( data_dir + "carts.p", "rb" ) )
else:
    carts = {}
    pickle.dump(carts, open( data_dir + "carts.p", "wb" ) )
    
sessions = pickle.load( open( data_dir + "sessions.p", "rb" ) )

t = open('cart.html')
template = t.read()
t.close()

def addItem(username, pic, name, price, status, seller, template):
    if not username in list(carts.keys()):
        carts[username] = []
    item = Item(username, pic, name, price, status, seller)
    carts[username].append(item)
    
    pickle.dump(carts, open( data_dir + "carts.p", "wb" ) )
    
    message = ('Successfully added {name}'.format(name=item.name))
    return fill_class(template, 'message', message)
    
def removeItem(username, rm_name, template):
    try:
        for item in carts[username]:
            if item.name == rm_name:
                item.remove()
                pickle.dump(carts, open( data_dir + "carts.p", "wb" ) )
                message = ('Successfully removed {name}'.format(name=item.name))
                return fill_class(template, 'message', message)
    except:
        AttributeError

if 'sid' in inpts and 'username' in inpts:
    sid = inpts.getvalue('sid')
    username = inpts.getvalue('username')
    if 'add_pic' in inpts and 'add_name' in inpts and 'add_price' in inpts and 'add_status' in inpts and 'add_seller' in inpts:
        username = inpts.getvalue('username')
        pic = inpts.getvalue('add_pic')
        name = inpts.getvalue('add_name')
        price = inpts.getvalue('add_price')
        status = inpts.getvalue('add_status')
        seller = inpts.getvalue('add_seller')
        template = addItem(username, pic, name, price, status, seller, template)
        
    if 'rm_name' in inpts:
        rm_name = inpts.getvalue('rm_name')
        template = removeItem(username, rm_name, template)
    content = ''
    if not username in list(carts.keys()):
        carts[username] = []
    for item in carts[username]:
        content += '''
    <div class="cart_item">
            <div class="cart_item_picture">
              <img src="{img}" alt="">
            </div>
            <div class="cart_info_container">
              <div class="cart_item_name">
                {name}
              </div>
              <div class="cart_item_price">
                ${price}
              </div>
              <div class="cart_item_seller">
                {seller}
              </div>
              <div class="cart_item_status">
                {status}
              </div>
              <div class="cart_item_remove">
                <form action="cart.py" method="POST">
                  <input type="hidden" name="sid" value="{sid}">
                  <input type="hidden" name="username" value="{username}">
                  <input type="hidden" name="rm_name" value="{name}">
                  <button type="submit" name="button" formaction="cart.py" class="rm_btn"><i class="fas fa-minus"></i> Remove From Cart</button>
                </form>
              </div>
            </div>
          </div>
'''.format(
    img=item.pic,
    name=item.name,
    seller=item.seller,
    status=item.status, 
    price=item.price,
    sid=sid,
    username=username,
    rm_name=item.name
    )
    
    try:
        template = fill_class(template, 'cart_items', content)
        template = template.format(
            username=sessions[sid].username,
            sid=sid,
            num_items_cart=len(carts[sessions[sid].username]),
            cart_total=cartTotal(sessions[sid].username)
            )
    except:
        AttributeError
    print(template)
else:
    print(redirect)

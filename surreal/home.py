#!/usr/bin/python
import cgi, cgitb, pickle, os, html, time, hashlib, scraperV2
import os.path as path

print("Content-type: text/html\n")

cgitb.enable()

headers = ['name', 'seller', 'price', 'status', 'link', 'image'] 
inpts = cgi.FieldStorage()

data_dir = ''

user_ip = html.escape(os.environ["REMOTE_ADDR"])
user_browser = html.escape(os.environ["HTTP_USER_AGENT"])

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

if path.exists(data_dir + "carts.p"):
    carts = pickle.load( open( data_dir + "carts.p", "rb" ) )
else:
    carts = {}
    pickle.dump(carts, open( data_dir + "carts.p", "wb" ) )

def clean_data(file):
    
    f = open(file) 
    d = f.read()
    f.close()

    d = d.split('\n')[1:-1]
    for i in range(len(d)):
        d[i] = d[i].split(",")
    return d


def get_column(key, headers, row):

    col = headers.index(key) 
    return row[col]


def search_name_brand(name_input, actual_name):

    return name_input in actual_name


def search_price(price_input, actual_price):

    return float(actual_price) <= float(price_input)

def search_store(store_input, actual_store):

    if store_input == None:
        return True

    return store_input == actual_store

def search_status(status_input, actual_status):

    if status_input == None:
        return True

    return status_input == actual_status


def search(fields):

    data = clean_data('data.csv')
    results = []

    for row in data:
        price_match = brand_match = name_match = status_match = True
        for field in fields:

            if field == 'price':
                try:
                    if fields[field] != 'NA':
                        actual_price = get_column('price', headers, row)
                        price_match = search_price(fields['price'], actual_price)
                    else:
                        price_match = True
                except TypeError:
                    pass

            elif field == 'brand':
                try:
                    if fields[field] != 'NA':
                        actual_name = get_column('name', headers, row)
                        brand_match = search_name_brand(fields['brand'], actual_name)
                    else:
                        brand_match = True
                except TypeError:
                    pass

            elif field == 'name':
                try:
                    if fields[field] != None:
                        actual_name = (get_column('name', headers, row)).lower()
                        name_match = search_name_brand((fields['name']).lower(), actual_name)
                    else:
                        name_match = True
                except TypeError:
                    pass

            elif field == 'status':
                try:
                    if fields[field] != 'NA':
                        actual_status = get_column('status', headers, row)
                        status_match = search_status(fields['status'], actual_status)
                    else:
                        status_match = True
                except TypeError:
                    pass
            elif field == 'store':
                try:
                    if fields[field] != 'NA':
                        actual_store = get_column('seller', headers, row)
                        store_match = search_store(fields['store'], actual_store)
                    else:
                        store_match = True
                except TypeError:
                    pass

        if price_match and name_match and store_match and brand_match and status_match:
            results.append(row)

    return results


def fill_class(html, cls, content):
    cls_pos = html.find('class=' + '"{cls}"'.format(cls=cls))
    if cls_pos != -1:
        content_start = cls_pos + html[cls_pos + 1:].find('>') + 2
        html = html[:content_start] + content + html[content_start:]
        return html

def low_to_high(d):
    return sorted(d, key=lambda x: float(x[2]), reverse=True)
def high_to_low(d):
    return sorted(d, key=lambda x: float(x[2]), reverse=False)
def alphabetical(d):
    return sorted(d, key=lambda x: x[0], reverse=True)
def reversed_alphabetical(d):
    return sorted(d, key=lambda x: x[0], reverse=False)

t = open('main.html')
template = t.read()
t.close()

def selected_option(field, key, html):
    select_loc = html.find('<select id="' + field + '" ' +'name="' + field + '">')
    option_loc = html[select_loc:].find('value="'+ key + '"') + select_loc
    return html[:option_loc] + ' selected ' + html[option_loc:]

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

if 'sid' in inpts:
    sid = inpts.getvalue('sid')
    sessions = pickle.load( open( data_dir + "sessions.p", "rb" ) )
    
    if sid in list(sessions.keys()) and sessions[sid].browser == user_browser:
        user_hashed_ip = hashlib.pbkdf2_hmac('sha256', user_ip.encode(), sessions[sid].ip_salt.encode(), 100000).hex()
        if sessions[sid].ip == user_hashed_ip:
            if time.time() <= 3600 + sessions[sid].start_time:
                if not sessions[sid].username in list(carts.keys()):
                    carts[sessions[sid].username] = []
                    
                if 'brand' in inpts or 'price' in inpts or 'status' in inpts or 'product_search' in inpts:
                    name = inpts.getvalue('product_search')
                    brand = inpts.getvalue('brand')
                    price = inpts.getvalue('price')
                    status = inpts.getvalue('status')
                    store = inpts.getvalue('store')
                    sort = inpts.getvalue('sort')

                    inpt_dict = {'name': name, 'store': store, 'brand':brand, 'price': price, 'status':status}
                    
                    template = selected_option('sort', sort, template)
                    template = selected_option('brand', brand, template)
                    template = selected_option('price', price, template)
                    template = selected_option('status', status, template)
                    template = selected_option('store', store, template)
                    
                    data = search(inpt_dict)
                else:
                    data = clean_data('data.csv')

                if 'sort' in inpts:
                    sort = inpts.getvalue('sort')
                    if sort == 'Lowest to Highest Price':
                        data = low_to_high(data)
                    elif sort == 'Highest to Lowest Price':
                        data = high_to_low(data)
                    elif sort == 'Alphabetical Order':
                        data = alphabetical(data)
                    elif sort == 'Reversed Alphabetical Order':
                        data = reversed_alphabetical(data)
                else:
                    data = low_to_high(data)
                    
                row_num = 0

                for row in data:
                    row_num += 1
                    item_content = """
                    <div class="item">
                        <div class="item_picture">
                            <img src="{img}" alt="">
                        </div>
                        <div class="item_name">
                            <a href={link}>{name}</a>
                        </div>
                        <div class='item_name'>
                            {seller}
                        </div>
                        <div class="status">
                            {status}
                        </div>
                        <div class="item_price">
                            ${price}
                        </div>
                        <div class="item_add_cart">
                          <button type="submit" name="button" form="{form_number}" formaction="cart.py" class="add_cart_btn"><i class="fas fa-plus"></i> Add to Cart</button>
                        </div>
                    </div>
                    """.format(name=row[0], seller=row[1], price=row[2], status=row[3], link=row[4], img=row[-1], form_number=('form'+str(row_num)))
                    if row[3] == None or row[3] == "":
                        status = ' '
                    else:
                        status = row[3]
                    template = fill_class(template, 'results', item_content)
                    item_forms = """
                        <form action="cart.py" method="POST" id="{form_number}">
                          <input type="hidden" name="sid" value="{sid}">
                          <input type="hidden" name="username" value="{username}">
                          <input type="hidden" name="add_pic" value="{img}">
                          <input type="hidden" name="add_name" value="<a href={link}>{name}</a>">
                          <input type="hidden" name="add_seller" value="{seller}">
                          <input type="hidden" name="add_status" value="{status}">
                          <input type="hidden" name="add_price" value="{price}">
                        </form>
                    """.format(name=row[0], seller=row[1], price=row[2], status=status, link=row[4], img=row[-1], form_number=('form'+str(row_num)), username=sessions[sid].username,
                            sid=sid)
                    template = fill_class(template, 'hidden_forms', item_forms)
                
                def cartTotal(username):
                    total = 0.00
                    for item in carts[username]:
                        total += float(item.price)
                    return "%0.2f" % total
                
                filled = template.format(
                    username=sessions[sid].username,
                    sid=sid,
                    num_matching_products=len(data),
                    num_items_cart=len(carts[sessions[sid].username]),
                    cart_total=cartTotal(sessions[sid].username)
                    )
                print(filled)
            else:
                scraperV2.write_csv()
                sessions[sid].end()
                print(redirect)
        else:
            scraperV2.write_csv()
            print(redirect)
    else:
        scraperV2.write_csv()
        print(redirect)
else:
    scraperV2.write_csv()
    print(redirect)

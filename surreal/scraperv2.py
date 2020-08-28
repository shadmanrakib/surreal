#!/usr/bin/python
from bs4 import BeautifulSoup
#from urllib.request import urlopen
import requests
import lxml
import time

seen = []

def clean_price(price):

    price = price.replace('$', '')
    price = float(price)
    return price


def get_WG(url):

    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')

    main_container = soup.find(class_='mb30 row wag-product-lists')
    
    for product in main_container.find_all(class_='col-xl-3 col-lg-3 col-md-6 col-sm-6 col-6 product-column pr0'):

        name_container = product.find(class_='sr-only')
        name = name_container.text.replace(',','')

        price_container = product.find(class_='product__price')
        price = clean_price(price_container.text)


def get_cvs(url, f):

    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')

    try:
        products_container = soup.find(class_='css-1dbjc4n')

        pagination = soup.find('a',class_='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1otgn73 r-eafdt9 r-1i6wzkk r-lrvibr')
        i = 0
        seen = []
        while True:

            for product in products_container.find_all(class_='css-1dbjc4n r-18u37iz r-tzz3ar'):
                
                product_data = product.find(class_='css-1dbjc4n r-13awgt0 r-1mlwlqe')

                name_container = product_data.find(class_='css-901oao css-cens5h r-1khnkhu r-1jn44m2 r-ubezar r-29m4ib r-rjixqe r-kc8jnq r-fdjqy7 r-13qz1uu')
                name = name_container.text.replace(',','')

                price_container = product_data.find(class_='css-901oao r-1jn44m2 r-evnaw r-b88u0q r-ttdzmv')
                price = clean_price(price_container.text)

                status_container = product_data.find(class_='css-901oao r-v857uc r-1jn44m2 r-1i10wst r-b88u0q')
                if status_container != None:
                    status = status_container.text.replace(',','')
                else:
                    status = ''

                link = 'https://www.cvs.com' + product.find('a')['href']

                img = product.find('img', class_='css-9pa8cd')['src']

                data = f"{name},CVS,{price},{status},{link},{img}\n"
                i += 1
                if data not in seen:
                    f.write(data)
                seen.append(data)
            
            pagination = soup.find('a',class_='css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1otgn73 r-eafdt9 r-1i6wzkk r-lrvibr')
            if pagination == None:
                break
            else:
                print('=================================================================')
                next_page = 'https://www.cvs.com/' + pagination['href']
                soup = BeautifulSoup(requests.get(next_page).content, 'lxml')
    except:
        pass


def get_bjs(url, f):

    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')

    try:

        for product in soup.find_all(class_='product'):

            name_container = product.find(class_='product-title no-select d-block d-sm-none')
            try:
                name = name_container['title'].replace(',','')
            except KeyError:
                name = name_container.text.replace(',','')

            price_container = product.find(class_='price')
            price = clean_price(price_container.text)

            link = 'https://www.bjs.com/' + product.find('a')['href']

            button_container = product.find(class_='red-btn height-each-btn')
            if button_container == None:
                status = 'Out of Stock'
            else:
                status = ''

            img = product.find(class_='img-link')['src']

            data = f"{name},BJ's,{price},{status},{link},{img}\n"
            f.write(data)
    except: 
        pass


def get_walmart(url, f):

    r = requests.get(url).content
    soup = BeautifulSoup(r, 'lxml')

    try:
        container = soup.find(class_='search-result-gridview-items four-items')

        for product in container('li'):
            
            name_container = product.find('a', class_='product-title-link line-clamp line-clamp-2 truncate-title')
            name = name_container.text.replace(',', '')
            
            link = 'https://www.walmart.com/' + name_container['href']
            
            try:
                price = clean_price(product.find(class_='price-characteristic').text + '.' + product.find(class_='price-mantissa').text)
                status = "Available Online"

                img_container = product.find('img')
                img = img_container['src']

                data = f"{name},Walmart,{price},{status},{link},{img}\n"
                f.write(data)
            except AttributeError:
                pass
    except:
        pass

def write_csv():

    print("Running")

    headers = ['name', 'seller', 'price', 'status', 'link', 'image'] 
    f = open('data.csv', 'w')
    for header in headers:
        f.write(header + ',')
    f.write('\n')

    urls = {'cvs': 'https://www.cvs.com/shop/household-grocery/paper-plastic-products/bath-tissue',
            'bjs': 'https://www.bjs.com/search/toilet%20paper/q?pagesize=80',
            'walmart': 'https://www.walmart.com/browse/household-essentials/toilet-paper/1115193_1073264_1149384?cat_id=1115193_1073264_1149384&facet=facet_product_type%3AToilet+Paper&stores=-1'}

    get_cvs(urls['cvs'], f)
    get_bjs(urls['bjs'], f)
    get_walmart(urls['walmart'], f)

    f.close()
    
    print("Done")

if __name__ == "__main__":
    write_csv()
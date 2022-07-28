from bs4 import BeautifulSoup
import requests
import pandas as pd
import socket
from urllib.parse import urlparse
import geoip2.database

# list of URLs
urls=[
    'https://www.ccn-cert.cni.es/component/obrss/rss-ultimas-vulnerabilidades.feed',
    'https://www.nist.gov/news-events/cybersecurity/rss.xml',
    'https://feeds.english.ncsc.nl/news.rss',
    'https://www.cert.ssi.gouv.fr/feed/',
    'https://cert.be/en/rss',
    'https://www.cshub.com/rss/categories/attacks',
    'https://www.cisa.gov/uscert/ncas/current-activity.xml'
    ]

# initialize list to hold data(title, date, etc..)
title = []
date = []
links = []
description = []
country = []

# first for loop to iterate through each URL and request content
# second for loop to iterate through each 'item' of the XML file and append data to initialized list
for url in urls:
    response = requests.get(url)
    content = BeautifulSoup(response.content, 'xml')
    items = content.find_all('item')

    for item in items:
        title.append(item.title.text)
        date.append(item.pubDate.text)
        links.append(item.link.text)
        description.append(item.description.text)

# finding location using geoip2 free database
for link in links:
    domain = urlparse(link).netloc
    ip = socket.gethostbyname(domain)
    with geoip2.database.Reader('GeoLite2-City.mmdb') as reader:
        response = reader.city(ip)
        country.append(response.country.name)

# create dataframe
data_frame = pd.DataFrame({'Title': title, 'Date published': date, 'Country':country, 'Link': links, 'Description': description})
print(data_frame.to_string())

# write to excel file
writer = pd.ExcelWriter('RSS.xlsx')
data_frame.to_excel(writer, sheet_name='mysheet')
workbook = writer.book
worksheet = writer.sheets['mysheet']
worksheet.set_column(1,1,80)
worksheet.set_column(2,2,30)
worksheet.set_column(3,3,15)
worksheet.set_column(4,5,120)
writer.save()



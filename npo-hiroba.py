#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import urllib
import tqdm

query = input ("Enter keyword: ")
file_name = input ("Enter output filename: ")
npo = pd.DataFrame(columns=['url','団体名','法人認証年月日','主たる事務所所在地','目的','事務局責任者','電話番号','fax','ホームページアドレス','ホームページの内容','email','活動開始の経緯','活動分野','事業内容'])
url = 'http://www.npo-hiroba.or.jp/search/result.php'

urlmax = urllib.parse.urljoin(url, 'result.php?c=search&WORD=' + str(query) )
response = requests.get(urlmax)
soup = BeautifulSoup(response.content, "html.parser")
try:
    num_pages = int(re.compile('\d+').search(soup.find('a',{'title' : "last page"}).string).group())
except Exception:
    try:
        num_pages = int(soup.find('a',{'title' : "page 2"}).string)
    except Exception:
        num_pages = 1

print( str(num_pages) + ' page(s) found!')
    
for i in tqdm.tqdm(range(num_pages), ascii=True, desc="Scraping search result"):
    url = urllib.parse.urljoin(url, 'result.php?c=search&WORD=' + str(query) )
    response = requests.post(url, data=dict(
    WORD= str(query),
    page= str(i+1) ))
    soup = BeautifulSoup(response.content, "html.parser")
    length = len(npo.index)
    for idx, link in enumerate(soup.find_all('table')[1].find_all("a", {"href": re.compile(r'zoom.php.*')})):
        npo = npo.append({'url':"http://www.npo-hiroba.or.jp/search/" + link.get("href")}, ignore_index=True)
        
for index, row in tqdm.tqdm(npo.iterrows(), ascii=True, desc="Scraping NPO profile"):
    url = npo['url'][index]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Scraping NPO name
    try:
        name = soup.find('table', {'class':'registration'}).find('th', text='団体名').findNext('td').get_text(strip=True)
        npo['団体名'][index] = name
    except Exception:
        npo.at[row.name, '団体名'] = 'NA'
        
    table1 = soup.find('div', {'id':'fragment-1'}).find('table', {'class':'infotable'})
    try:
        est = ''.join(table1.find('th', text='法人認証年月日').findNext('td').get_text().split())
        npo['法人認証年月日'][index] = est
    except Exception:
        npo.at[row.name, '法人認証年月日'] = 'NA'
    try:
        adr = ''.join(table1.find('th', text='主たる事務所所在地').findNext('td').get_text().split())
        npo['主たる事務所所在地'][index] = adr
    except Exception:
        npo.at[row.name, '主たる事務所所在地'] = 'NA'
    try:
        aim = ''.join(table1.find('th', text='目的').findNext('td').get_text().split())
        npo['目的'][index] = aim
    except Exception:
        npo.at[row.name, '目的'] = 'NA'
    try:
        pic = ''.join(table1.find('th', text='事務局責任者').findNext('td').get_text().split())
        npo['事務局責任者'][index] = pic
    except Exception:
        npo.at[row.name, '事務局責任者'] = 'NA'
    try:
        tel = ''.join(table1.find('th', text='電話番号').findNext('td').get_text().split())
        npo['電話番号'][index] = tel
    except Exception:
        npo.at[row.name, '電話番号'] = 'NA'
    try:
        fax = ''.join(table1.find('th', text='FAX').findNext('td').get_text().split())
        npo['fax'][index] = fax
    except Exception:
        npo.at[row.name, 'fax'] = 'NA'
    try:
        web = ''.join(table1.find('th', text='ホームページアドレス').findNext('td').get_text().split())
        npo['ホームページアドレス'][index] = web
    except Exception:
        npo.at[row.name, 'ホームページアドレス'] = 'NA'
    try:
        webdesc = ''.join(table1.find('th', text='ホームページの内容').findNext('td').get_text().split())
        npo['ホームページの内容'][index] = webdesc
    except Exception:
        npo.at[row.name, 'ホームページの内容'] = 'NA'
    try:
        email = ''.join(table1.find('th', text='E-Mail').findNext('td').get_text().split())
        npo['email'][index] = email
    except Exception:
        npo.at[row.name, 'email'] = 'NA'
        
    table2 = soup.find('div', {'id':'fragment-2'}).find('table', {'class':'infotable'})
    try:
        background = ''.join(table2.find('th', text='活動開始の経緯').findNext('td').get_text().split())
        npo['活動開始の経緯'][index] = background
    except Exception:
        npo.at[row.name, '活動開始の経緯'] = 'NA'
    try:
        area = ''.join(table2.find('th', text='活動分野').findNext('td').get_text().split())
        npo['活動分野'][index] = area
    except Exception:
        npo.at[row.name, '活動分野'] = 'NA'
    try:
        activity = ''.join(table2.find('th', text='事業内容').findNext('td').get_text().split())
        npo['事業内容'][index] = activity
    except Exception:
        npo.at[row.name, '事業内容'] = 'NA'    
    try:
        keyword = ''.join(table2.find('th', text='活動キーワード').findNext('td').get_text().split())
        npo['活動キーワード'][index] = keyword
    except Exception:
        npo.at[row.name, '活動キーワード'] = 'NA'  

npo.to_csv(file_name + '.csv', encoding='utf-8')
print('Finished!')

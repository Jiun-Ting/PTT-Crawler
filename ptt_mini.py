from bs4 import BeautifulSoup
import requests as rq
import random
from time import sleep
import re
import warnings
import json
warnings.filterwarnings('ignore')

#path, initail setting
board = 'creditcard'
page_amount = 200
lag = 10

if 'over18' in rq.get('https://www.ptt.cc/bbs/{}/index.html'.format(board), verify=False).url:
    rq = rq.session()
    payload = {'from':'	/bbs/{}/index.html'.format(board), 'yes':'yes'}
    Goal = rq.post('https://www.ptt.cc/ask/over18', data = payload, verify=False)

Goal = rq.get('https://www.ptt.cc/bbs/{}/index.html'.format(board), verify=False)
soup = BeautifulSoup(Goal.text)
former_page = soup.select('.btn.wide')[1]['href']
start_page = int(re.findall('^index([0-9]+).*',former_page.split('/')[-1])[0])+1-lag


index_list = []
soup = []
for page in range(start_page, start_page - page_amount, -1):
    page_url = 'https://www.ptt.cc/bbs/{}/index{}.html'.format(board, page)
    index_list.append(page_url)

for page in index_list:
    Goal = rq.get(page, verify=False)
    soup.append(BeautifulSoup(Goal.text))


#metadata
articles = []
date = []
author = []
nrec = []
title = []

Main = []
Mild = []
Pos = []
Neg = []
N_Re = []

for i in range(len(soup)):
    for entry in soup[i].select('.r-ent'):
        try :
            if (u'公告' not in (entry.select('.title')[0].text.strip())) and (u'刪除' not in (entry.select('.title')[0].text.strip())):
                articles.append(BeautifulSoup(rq.get("https://www.ptt.cc/"+entry.select('.title')[0]('a')[0].get('href', None), verify=False).text))
                title.append(entry.select('.title')[0].text.strip())
                author.append(entry.select('.meta')[0].select('.author')[0].text)
                nrec.append(entry.select('.nrec')[0].text)
                date.append(entry.select('.meta')[0].select('.date')[0].text)
                time = random.uniform(0, 1)/5
                sleep(time)
        except:
            print('deleted')
    print("finished: ",100*i/len(soup),"%")

#text
for article in articles:
    try:
        content = article.find(id="main-content").text
    except: #No content
        content = "None"        
    try:
        content = content.split(u'※ 發信站: 批踢踢實業坊(ptt.cc),')
    except: #Editted   
        content = content.split(u'※ 編輯')
    try:
        full_date = article.select('.article-meta-value')[3].text        
        main = content[0].split(full_date)[1].replace('\n',' ').replace('\t',' ')
    except: #If no date, no need to split
         main = content[0].replace('\n',' ').replace('\t',' ')
    Main.append(main.strip())
    for ch in main:
        if ch in ['\n','\t']:
            Main.append(main.replace(ch, ' '))
#comments
    mild = []
    pos = []
    neg = []
    n_Re = 0
    try:  
        push = content[1].split('\n')
        for item in push:
            if re.search(u'^推' ,item):
                pos.append(' '.join(item[item.find(':')+2:].split(' ')[:-2]))
            elif re.search(u'^→' ,item):
                mild.append(' '.join(item[item.find(':')+2:].split(' ')[:-2]))
            elif re.search(u'^噓' ,item):
                neg.append(' '.join(item[item.find(':')+2:].split(' ')[:-2]))
        n_Re = len(pos)+len(neg)+len(mild)
   
        Pos.append(pos)
        Neg.append(neg)
        Mild.append(mild)
        N_Re.append(n_Re)
    except:
        Pos.append("None")
        Neg.append("None")
        Mild.append("None")
        N_Re.append("None")        
        
        
#check articles and metadata        
for i in range(len(title)):
    print(date[i], nrec[i], author[i], title[i])
print('\n')    
print(date[0], nrec[0], author[0], title[0])
print('\n')
print(Main[0])
print('\n')
print(Pos[0])
print(Mild[0])
print(Neg[0])


#check comments
for i in range(len(Neg)):
    if len(Neg[i])>0:
        print(Neg[i])

for i in range(len(Pos)):
    if len(Pos[i])>0:
        print(Pos[i])  
    
    
#create dictrionary
database = []
for i in range(len(title)):
    database.append({"title": title[i],
             "author": author[i],
             "N_rec": N_Re[i],
             "article": Main[i],
             "Mild": Mild[i],
             "Pos": Pos[i],
             "Neg": Neg[i]
             }
    )
    
#export data as json        
with open('data_{}.json'.format(board), 'w', encoding='utf-8') as f:
    json.dump(database, f, indent=2, sort_keys=True, ensure_ascii=False)

import json
import jieba

#Input data from json
board = 'EAseries'
with open('data_{}.json'.format(board), 'r',encoding='utf-8') as f:
    data = json.load(f)

#Input stop words list
stop = []
fh =  open('C:/Users/ROBIN/Desktop/pytest/stopea.txt', 'r',encoding='utf-8')
for i in fh:
    stop.append(i.strip())

#Combine title, content and comments of each postings and segment sentences by jieba
Corpus = []
for i in data:
    a_word = []
    t_word = []
    M_word = []
    N_word = []
    P_word = []
    corpus = []      
    a_word += jieba.cut(i['article'], cut_all = False)     
    t_word += jieba.cut(i['title'], cut_all = False)    
    for j in i['Mild']:        
        M_word += jieba.cut(j, cut_all = False)
    for j in i['Neg']:  
        N_word += jieba.cut(j, cut_all = False)
    for j in i['Pos']:          
        P_word += jieba.cut(j, cut_all = False)
    corpus = a_word + t_word + M_word + N_word + P_word
    corpus = ' '.join(corpus)
    Corpus.append(corpus)

#transform the segmented words to tf-idf, representing each postings
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(max_features = 10000, strip_accents='unicode',
                        lowercase =True, analyzer='word', use_idf=True, 
                        smooth_idf=True, sublinear_tf=True, stop_words = stop)
NewC = tfidf.fit_transform(Corpus)

#cluster postings by kmeans 
from sklearn.cluster import KMeans
import numpy as np
num_sort = 9
tops = 10
kmeans = KMeans(n_clusters= num_sort).fit(NewC)
kmeans.labels_

#sum the tf-idf of postings by cluster
Sort = {}
for i in range(len(kmeans.labels_)):
    Sort[kmeans.labels_[i]] = None
for i in range(len(kmeans.labels_)):
    if Sort[kmeans.labels_[i]] == None:
        Sort[kmeans.labels_[i]] = NewC[i]
    else:
        Sort[kmeans.labels_[i]] += NewC[i]

#get the percentage of each cluster
per = {}
for i in range(len(kmeans.labels_)):
    per[kmeans.labels_[i]] = None
for i in range(len(kmeans.labels_)):
    for j in range(num_sort):
        if kmeans.labels_[i]==j:
            if  per[kmeans.labels_[i]] == None:
                per[kmeans.labels_[i]] = 1
            else:
                per[kmeans.labels_[i]] +=1 
for k, v in per.items():
    print(k,100*v/len(kmeans.labels_))


#print top 10 tf-idf of each cluster 
top10 = []
for i in range(num_sort):
    lst = []
    temp = []
    scores = zip(tfidf.get_feature_names(),
                 np.asarray(Sort[i].sum(axis=0)).ravel())
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    for item in range(tops):
        print(sorted_scores[item][0])
        temp.append((sorted_scores[item][0]))
    top10.append(temp)
    print("\n")

#get the title of postings by cluster
t_word = []
for i in data:
    t_word.append(i['title'])    
Title = {}
for i in range(len(kmeans.labels_)):
    Title[kmeans.labels_[i]] = []
for i in range(len(kmeans.labels_)):
    Title[kmeans.labels_[i]].append(t_word[i])

#random select the title of each clusting to check the clustering result  
num = 20
from random import randint
for i in range(len(Title)):
    for _ in range(num):
        print(Title[i][randint(0, len(Title[i]))])
    print('\n')
    


import json
import jieba

#import json-data
board = 'EAseries'
with open('data_{}.json'.format(board), 'r',encoding='utf-8') as f:
    data = json.load(f)

#import stop words list
stop = []
fh =  open('C:/Users/ROBIN/Desktop/pytest/stopea.txt', 'r',encoding='utf-8')
for i in fh:
    stop.append(i.strip())

#combine title, main content, and commets of each postings and segment them by jieba
a_word = []
t_word = []
M_word = []
N_word = []
P_word = []
Corpus = []
for i in data:
    a_word += jieba.cut(i['article'])
    t_word += jieba.cut(i['title'])
    for j in i['Mild']:        
        M_word += jieba.cut(j, cut_all = False)
    for j in i['Neg']:  
        N_word += jieba.cut(j, cut_all = False)
    for j in i['Pos']:  
        P_word += jieba.cut(j, cut_all = False)

Corpus = a_word + t_word + M_word + N_word + P_word

#Count the number of appearance of each word 
table = dict()
for i in Corpus:
    if i not in table:
        table[i] = 1;
    else:
        table[i] += 1;
nb = dict()
for k, v in table.items():
    nb[v] = k

#print the result by ordre (from high freqency to low)
List = []
lst = sorted(nb.items(), reverse = True)
for i in lst:
    if (len(i[1])>= 2) and (i[1] not in stop):
        List.append((i[1], i[0]))
for i in range(len(List)):
    print(List[i][0], List[i][1])
        



# PTT-Crawler and Text Clustering
The python codes under this repository includes three parts.

ptt\_mini.py: Focus on crawling the main metadata and text content of the postings of the board specified. The crwaling data is stored to a json file. The json file includes title, author, posting date, number of comments, main content and comments of each postings.

ptt\_cluster.py: Cluster the postings by k-means and list the results and the keywords by cluster.

ptt\_cloud.py: Output the number of apperance of each word.

stopea.txt: Stop words used to analyze the borad EAseries.  

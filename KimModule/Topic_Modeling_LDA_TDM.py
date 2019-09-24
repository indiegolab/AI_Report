import pandas as pd
from gensim import corpora
import gensim

class Topic_LDA_TDM:
    def __init__(self,news_doc_ls):
        self.news_doc_ls = news_doc_ls
        
    def LDA_TDM(self):
        news_doc_ls = self.news_doc_ls
        
        new_doc = [doc.split(',') for doc in news_doc_ls]
        
        dictionary = corpora.Dictionary(new_doc)  #단어를 인덱스화 하는것
        
        corpus = [dictionary.doc2bow(text) for text in new_doc]   #TDM으로 만들겠다. 
        
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 10, id2word = dictionary, passes=5)

        topics = ldamodel.print_topics(num_words=10)
        for topic in topics:
            print(topic)
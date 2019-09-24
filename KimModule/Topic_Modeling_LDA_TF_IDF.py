import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaModel
from gensim.models import TfidfModel
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt


class Topic_LDA_TF_IDF:
    def __init__(self,news_doc_ls):
        self.news_doc_ls = news_doc_ls
        self.news_doc = [doc.split(',') for doc in news_doc_ls]
        #dic = corpora.Dictionary(news_doc)
        self.dictionary = corpora.Dictionary(self.news_doc)
        self.corpus = [self.dictionary.doc2bow(text) for text in self.news_doc]
        tfidf_model = TfidfModel(self.corpus)
        self.corpus = tfidf_model[self.corpus]
        
    def Topic_Num_Decision(self, start, stop, size):
        
        model_list = []
        coherence_values = []
        topic_n_list = []
        perplexity_values = []
        

        for num_topics in range(start, stop, size):
            model = LdaModel(self.corpus, num_topics=num_topics, id2word = self.dictionary)
            model_list.append(model)

            coherencemodel = CoherenceModel(model=model, texts=self.news_doc, dictionary=self.dictionary, coherence='c_v')
            coherence_values.append(coherencemodel.get_coherence())
            topic_n_list.append(num_topics)
            perplexity_values.append(model.log_perplexity(self.corpus))
            
        return model_list, coherence_values, perplexity_values
    
    
    def Topic_Num_Decision_Plt(self, start, stop, size):

        model_list, coherence_values, perplexity_values = self.Topic_Num_Decision(start, stop, size)
        x = range(start, stop, size)
        fig, ax1 = plt.subplots()
        color = 'tab:blue'
        ax1.set_xlabel("Number of Topics")
        ax1.set_ylabel("Coherence score", color=color)
        ax1.plot(x, coherence_values, color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:red'
        ax2.set_ylabel('Perplexity score', color=color)  # we already handled the x-label with ax1
        ax2.plot(x, perplexity_values, color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()
    
    
    
    def LDA_TF_IDF(self,num_topics):
        
        ldamodel = gensim.models.ldamodel.LdaModel(self.corpus, num_topics = num_topics, id2word = self.dictionary, passes=5)

        topics = ldamodel.print_topics(num_words=10)
        for topic in topics:
            print(topic)
            

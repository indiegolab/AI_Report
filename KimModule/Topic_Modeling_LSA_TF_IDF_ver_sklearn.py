from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import randomized_svd

class Topic_LSA_TF_IDF:
    def __init__(self,doc_ls):
        self.doc_ls = doc_ls
        
    def LSA_TF_IDF(self):
        doc_ls = self.doc_ls
    
        #sklearn TF-IDF
        
        
        def TF_IDF(doc_ls):
            def tokenizer(doc):
                return doc.split(',')
            
            vectorizer = TfidfVectorizer(max_features = 1000, max_df = 0.5, smooth_idf = True, tokenizer = tokenizer)
            tf_idf = vectorizer.fit_transform(doc_ls)
            term =  vectorizer.get_feature_names()
            return tf_idf,term

        tf_idf, terms = TF_IDF(doc_ls)
        #tf_idf.toarray()

        # 특이값 분해
        def SVD(tf_idf):
            U, s, VT = randomized_svd(tf_idf,n_components=10,n_iter=5,random_state=None)
            #U, s, VT = np.linalg.svd(tdm)
            return U, s, VT

        U_tfidf, s_tfidf, VT_tfidf = SVD(tf_idf)

        # 토픽 모델링
        def get_topics(components, feature_names, n=10):
            for idx, topic in enumerate(components):
                print("Topic %d: " % (idx+1),
                     [(feature_names[i], topic[i].round(5)) for i in topic.argsort()[:-n-1:-1]])



        print("TF_IDF토픽모델링")        
        get_topics(VT_tfidf, terms)  # 행/렬반대로 되있어서 transfer해줘야함.

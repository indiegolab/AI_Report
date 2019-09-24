from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import randomized_svd

class Topic_LSA_TDM:
    def __init__(self,doc_ls):
        self.doc_ls = doc_ls
        
    def LSA_TDM(self):
        doc_ls = self.doc_ls

        #sklearn TDM
        def TDM(doc_ls):
            def tokenizer(doc):
                return doc.split(',')

            vectorizer_TDM = CountVectorizer(min_df = 1,tokenizer = tokenizer)
            tdm = vectorizer_TDM.fit_transform(doc_ls)
            terms =  vectorizer_TDM.get_feature_names()
            #Y.toarray()
            return tdm,terms
        tdm, terms = TDM(doc_ls)
        #tdm.toarray()



        # 특이값 분해
        def SVD(tdm):
            U, s, VT = randomized_svd(tdm, n_components=10,n_iter=5,random_state=None)
            #U, s, VT = np.linalg.svd(tdm)
            return U, s, VT

        U_tdm, s_tdm, VT_tdm = SVD(tdm)

        # 토픽 모델링
        def get_topics(components, feature_names, n=10):
            for idx, topic in enumerate(components):
                print("Topic %d: " % (idx+1),
                     [(feature_names[i], topic[i].round(5)) for i in topic.argsort()[:-n-1:-1]])


        print("TDM토픽모델링")
        get_topics(VT_tdm, terms)
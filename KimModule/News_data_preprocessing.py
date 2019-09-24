import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import bigrams
from nltk import trigrams
from nltk.util import ngrams
from konlpy.tag import Mecab
from ekonlpy.sentiment import MPCK

class News_PreProcessing:
        
        def __init__(self,news):
            self.news = news

        def content_pre(self,file_name=''):
            news = self.news
            
            news = news.dropna()
            news = news.reset_index()
            del news['index']
            #del news['url']
            #del news['Unnamed: 0']

            media_name = news['media'].unique()
            media_name = str(list(media_name))
            media_name = media_name.replace("[","'(").replace("]",")'").replace("'","").replace(", ","|")
            
            def func(x):
                tmp0 = re.sub(media_name," ",x)
                return tmp0
            
            news['content'] = news['content'].map(lambda x : func(x))
            
            def func(x):
                return re.sub(r'[-=+,#/\?:^$*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》;▲△↑↓’·“”ⓒㅡㅠ▣▶◇_/{/}【】◆★■「」]','',x).strip()  
            
            news['content'] = news['content'].map(lambda x : func(x))
            news['title'] = news['title'].map(lambda x : func(x))
            
            def func(x):
                tmp0 = re.sub(r'(\n|\t)','',x)
                tmp1 = re.sub(r'(무단전재 및 재배포금지|무단 전재재배포 금지|무단 전재 및 재배포 금지)','',tmp0)
                tmp2 = re.sub(r'무단전재 및 재배포 금지','',tmp1)
                tmp3 = re.sub(r'[a-zA-Z0-9]+\@[a-zA-Z0-9]+\.[a-z]{1,3}\.[a-z]{1,3}','',tmp2)
                tmp4 = re.sub(r'[a-zA-Z0-9]+\@[a-zA-Z0-9]+\.[a-z]{1,3}','',tmp3)
                tmp5 = re.sub(r'[a-zA-Z0-9]+\.[a-z]{1,3}','',tmp4)
                tmp6 = re.sub(r'＜종합 경제정보 미디어    무단전재  재배포 금지＞','',tmp5)
                tmp7 = re.sub(r'(동영상 뉴스|클릭|눌러보기|네이버에서|네이버|채널에서|구독해주세요|구독하기|한경닷컴|서울신문|모바일한경|구독신청|뉴스|저작권자|기자|Copyrights|미디어넷|구독하기꿀잼가득|영상보기|네이버 홈에서|한겨레|정기구독|한겨레신문|청춘뉘우스 스냅타임|바로가기)','',tmp6)
                tmp8 = re.sub(r'●','',tmp7)
                tmp9 = re.sub(r'(①|②|③)','',tmp8)
                tmp10 = tmp9.strip()
                return tmp10
            
            news['content'] = news['content'].map(lambda x : func(x))


            if file_name !='':
                news.to_csv(file_name,encoding='utf-8')
                
            self.news = news
            
            return news
        
        def tokens_ngram(self,file_name=''):
            #mecab = Mecab()
            mpck = MPCK()
            news = self.news
            
            tokens_list=[]
            news['tokens']=''
            news['bigram']=''
            news['trigram']=''
            news['fourgram']=''
            news['fivegram']=''
            news['ngram']=''
            
            for i in range(len(news)):
                try:
                    tokens = mpck.tokenize(news['content'][i])
                    #tokens = mecab.tokenize(news['content'][i])
                    tokens = [token.lower() for token in tokens if len(token.split('/')[0]) > 1]
                    
                    news['tokens'][i] = ','.join(tokens)


                    bi_gram = [';'.join(ngram) for ngram in ngrams(tokens,2)]
                    news['bigram'][i] = ','.join(bi_gram)

                    tri_gram = [';'.join(ngram) for ngram in ngrams(tokens,3)]
                    news['trigram'][i] = ','.join(tri_gram)

                    four_gram = [';'.join(ngram) for ngram in ngrams(tokens,4)]
                    news['fourgram'][i] = ','.join(four_gram)

                    five_gram = [';'.join(ngram) for ngram in ngrams(tokens,5)]
                    news['fivegram'][i] = ','.join(five_gram)

                    if file_name !='':
                        news.to_csv(file_name,encoding = 'utf-8', mode='a')
                except Exception as e:
                    print(e)
                    pass
            
            news['ngram']=news['bigram']+news['trigram']+news['fourgram']+news['fivegram']
            

            
            if file_name !='':
                news.to_csv(file_name,encoding='utf-8')
            
            return news
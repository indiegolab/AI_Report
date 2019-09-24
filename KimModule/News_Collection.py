import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

class News_Collect:
    def __init__(self,keywords,startdate,enddate):
        self.keywords = keywords
        self.startdate = startdate
        self.enddate = enddate
       
    
    def news_collect(self):
        keywords=self.keywords
        startdate = self.startdate
        enddate = self.enddate
        url = "http://211.180.114.181/newsapi/data"
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        params = {
               "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJncm91cCI6ImZpbmluc2lnaHQiLCJuYW1lIjoibWluaG8iLCJleHAiOjE1Nzc4MDQzOTkuMH0.BtwCRnyQeJ3vV5zQ_9zXzk_qZrtCfadcMt5y5Rgzw4U",
                    "pageNumber": 0,
                    "size": 1000,
                    "search":[
                        { "key": "body", "value": keywords }
                    ],
                    "order": {},
                        "filter": { "from": startdate, "to": enddate }
                }

        #print(url)
        response = requests.post(url, data=json.dumps(params), headers=headers, timeout=100)
        #print(response.text)

        try :
            result = json.loads(response.text)

        except Exception as e:
            print(response.text)
            print(str(e))

        df = pd.DataFrame(columns=['title', 'date', 'media', 'url', 'content'])

        for i in range(result["message"]["totalPages"]):
            params = {         "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJncm91cCI6ImZpbmluc2lnaHQiLCJuYW1lIjoibWluaG8iLCJleHAiOjE1Nzc4MDQzOTkuMH0.BtwCRnyQeJ3vV5zQ_9zXzk_qZrtCfadcMt5y5Rgzw4U",
                "pageNumber": i,
                "size": 1000,
                "search":[
                    { "key": "body", "value": keywords }
                ],
                "order": {},
                    "filter": { "from": startdate, "to": enddate }
            }

            response = requests.post(url, data=json.dumps(params), headers=headers, timeout=100)
            result = json.loads(response.text)
            for item in result["message"]["data"] :

                df.loc[len(df)] = [item["title"],
                                  item["reg_date"],
                                  item["origin_nm"],
                                  item["origin_url"],
                                  item["body"]]
                if df.shape[0] % 1000 == 0 :
                    print("{} / {}".format(item["reg_date"], df.shape[0]))

        df['date'] = pd.to_datetime(df['date'])
        df['type'] = 'news'
        df=df[['type','date','media','title','content','url']]
        
        
        return df
# -*- coding: utf-8 -*-
import scrapy
from dateutil.relativedelta import relativedelta
from datetime import date
import pandas as pd
from NewsCrawler.items import NewscrawlerItem
from urllib import parse
import requests
import re

class NavernewsSpider(scrapy.Spider):
    name = 'navernews'
    def start_requests(self):
        # years = getattr(self, 'years', 0)
        # months = getattr(self, 'months', 0)
        query = getattr(self, 'query', '')
        
        # making urls
        start = '20170101' # date.today()-relativedelta(years = years, months = months, days =1)
        end = '20190831' # date.today()-relativedelta(days = 1)
        for day in pd.date_range(start = start, end = end):
            day = day.strftime('%Y%m%d')
            url = 'https://search.naver.com/search.naver?where=news&query={0}&sort=0&pd=3&ds={1}&de={1}'.format(query, day)
            yield scrapy.Request(url=url, callback=self.parse)
            
    def parse(self, response):
        for tag in response.css('div.news ul.type01 li'):
            if tag.css('dd.txt_inline a._sp_each_url').get():
                href = tag.css('dd.txt_inline a::attr(href)').get()
                yield response.follow(href, self.naver_news)
        
        next_page = response.css('div.paging a.next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
    
    def naver_news(self, response):
        item = NewscrawlerItem()
        try:
            # basic information
            title = response.css('div.article_info h3#articleTitle::text').get()
            url = response.url
            date = response.css('div.article_info span.t11::text').get().split(' ')[0]
            press = response.css('div.press_logo a img::attr(title)').get()
            bodyList = response.css('div._article_body_contents *::text').getall()
            
            tempbody = ''.join(bodyList)
            pattern1 = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+.*)|  |\t|\n|\r|\xa0'
            pattern2 = r'\(?이 기사는 언론사에서.*'
            tempbody = re.sub(pattern1, '', tempbody)
            tempbody = re.sub(pattern2, '', tempbody)
            body = tempbody.replace('// flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback() {}','')

            # sentimental infomation
            pick_binary = response.css('div.head_channel::attr(style)').get()
            pick = 0 if 'none' in pick_binary else 1

            _url = parse.parse_qs(parse.urlsplit(response.url).query)
            oid = _url['oid'][0]
            aid = _url['aid'][0]

            react_url = 'https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&q=NEWS%5Bne_{0}_{1}%5D%7CNEWS_SUMMARY%5B{0}_{1}%5D%7CNEWS_MAIN%5Bne_{0}_{1}%5D&isDuplication=false'.format(oid,aid)
            react_resp=requests.get(react_url)
            react_json = react_resp.json()['contents'][0]['reactions']
            react = {}
            for i in range(len(react_json)):
                react[react_json[i]['reactionType']]=react_json[i]['count']
            recommend_json = react_resp.json()['contents'][2]['reactions']
            recommend = recommend_json[0]['count'] if recommend_json else 0

            comment_url = 'https://news.naver.com/api/comment/listCount.json?resultType=MAP&ticket=news&lang=ko&country=KR&objectId=news{0},{1}'.format(oid,aid)
            comment_resp = requests.get(comment_url)
            comment_json = comment_resp.json()['result']
            comment = list(comment_json.values())[0]['comment']

            # wrapping
            item['title'] = title
            item['url'] = url
            item['date'] = date
            item['press'] = press
            item['body'] = body
            item['pick'] = pick
            item['react'] = react
            item['comment'] = comment
            item['recommend'] = recommend
            
            yield item
        
        except:
            item['body'] = '에러'
            item['url'] = response.url

            yield item




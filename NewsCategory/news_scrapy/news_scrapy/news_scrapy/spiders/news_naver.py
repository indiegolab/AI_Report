# -*- coding: utf-8 -*-
import scrapy
import pandas
from news_scrapy.items import NewsScrapyItem
import requests
import re
from scrapy.selector import HtmlXPathSelector

class NewsNaverSpider(scrapy.Spider):
    name = 'news_naver'
    start_urls = []

    for sectionid in range(100,106): 
        dt_index = pandas.date_range(start='20170101', end='20191001')
        dt_list = dt_index.strftime("%Y%m%d").tolist()
        dt_list.reverse()
        for date in dt_list:
            url = 'https://news.naver.com/main/ranking/popularDay.nhn?rankingType=popular_day&sectionId={}&date={}'.format(sectionid, date)
            start_urls.append(url)
    
    def parse(self, response):
        print('response.url : ' + response.url)
        item = NewsScrapyItem()
        ol = response.css('ol.ranking_list')
        for li in ol:
            item['title'] = li.css('div.ranking_text div.ranking_headline ::attr(title)').get()
            item['cop'] = li.css('div.ranking_text div.ranking_office ::text').get()
            item['url'] = li.css('div.ranking_text div.ranking_headline a ::attr(href)').get()

            sectionsplit = response.url.split('sectionId=')
            sectionnum = sectionsplit[1][0:3]
            if sectionnum == '100':
                item['category'] = '정치'
            elif sectionnum == '101':
                item['category'] = '경제'
            elif sectionnum == '102':
                item['category'] = '사회'
            elif sectionnum == '103':
                item['category'] = '생활/문화'
            elif sectionnum == '104':
                item['category'] = '세계'
            elif sectionnum == '105':
                item['category'] = 'IT/과학'
            datesplit = response.url.split('date=')
            item['date'] = datesplit[1][0:8]
            item['eyes'] = li.css('div.ranking_text div.ranking_view ::text').get()
 
        yield item
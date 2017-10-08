# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings #从settings文件中导入Cookie，这里也可以室友from scrapy.conf import settings.COOKIE
from scrapy import Selector,Request
from TaoBaoScrapy.items import TaobaoscrapyItem
import  json
import re

class TaobaospiderSpider(RedisSpider):
    name = 'TaoBao'
    # start_urls = ['https://world.taobao.com/']
    redis_key = 'myspider:start_urls'

    # def start_requests(self):  #when extends RedisSpider ,use  middlewares.py(UserAgentMiddleware)
    #     yield scrapy.Request(url=self.redis_key[0],cookies=settings['cookies'])  # 这里带着cookie发出请求

    def parse(self, response):
        # print(str(response.body,'utf-8'))
        select = Selector(response)
        item=TaobaoscrapyItem()
        #猜你喜欢
        itemListDict=select.xpath('//div[@class="zebra-oversea-feeds-pc"]/div[@class="content"]/script/text()').extract_first()
        # print("-----itemListDict:"+itemListDict)
        itemList=json.loads(itemListDict)["itemList"] #str-->dict
        # print("-----itemList len:" + str(len(itemList)))
        i=1
        for imgdiv in itemList:
            if i<2:
                img=imgdiv['itemImg']
                actPrice=imgdiv['itemActPrice']
                mPrice = imgdiv['itemMPrice']
                tagPrice = imgdiv['itemTagPrice']
                title = imgdiv['itemTitle']
                url = imgdiv['itemUrl']
                item['img']=img
                item['actPrice'] =actPrice
                item['mPrice'] =mPrice
                item['tagPrice']=tagPrice
                item['title'] =title
                item['url'] =url
                yield Request("http:"+url,callback='details',meta={'item':item},dont_filter = True)
                i+=1
            else:
                break
    #跳转到下一网页
    def details(self,response):
        print("next url:------------>>>"+response.url)
        print(str(bytes(response.body).decode("gbk", 'ignore').encode("utf-8"),'utf-8'))
        # #https://item.taobao.com/world/item.htm?ft=t&toSi
        domain=re.search("https://(.*?).com",response.url,re.S).group(1)
        print("domin:---------->>>"+domain)
        item=response.meta['item']
        select=Selector(response)
        if domain=='item.taobao':#淘宝
            #店名
            shopName=select.xpath('//*[@id="J_ShopInfo"]/div[2]/div[1]/div[1]/dl/dd/strong/a/text()').extract_first()
            print("------淘宝---->>>shopName:" + shopName)
        else:#天猫
            shopName = select.xpath('//*[@id="shopExtra"]/div[1]/a/strong/text()').extract_first()
            print("------天猫---->>>shopName:"+shopName)
        yield item




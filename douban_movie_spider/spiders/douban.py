# -*- coding: utf-8 -*-
import scrapy
from douban_movie_spider.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'movie_top_250'
    start_urls = ['https://movie.douban.com/top250']
    # 如果有多个spider, 则通过custom_settings配置, 取代全局settings文件中的部分
    # 注意SaveImagePipeline的优先级应该要高于Save2MongoPipeline的优先级, 因为将电影海报保存到本地后, item还需要记录保存到本地的路径
    custom_settings = {
        'ITEM_PIPELINES': {
            'douban_movie_spider.pipelines.SaveImgPipeline': 100,
            'douban_movie_spider.pipelines.Save2MongoPipeline': 200,
        },
    }

    def parse(self, response):
        for item in response.css('div.item'):
            movie = MovieItem()
            rank = item.css('div.pic em::text').extract_first()
            title = item.css('div.info div.hd span.title::text').extract_first()
            star = item.css('div.star span.rating_num::text').extract_first()
            quote = item.css('p.quote span.inq::text').extract_first()
            url = item.css('div.pic a::attr("href")').extract_first()
            image_url = item.css('div.pic img::attr("src")').extract_first()
            movie['rank'] = rank
            movie['title'] = title
            movie['star'] = star
            movie['quote'] = quote
            movie['url'] = url
            movie['image_url'] = image_url
            yield movie

        # 获取下一页的url
        next_url = response.css('span.next a::attr("href")').extract_first()
        if next_url is not None:
            url = self.start_urls[0] + next_url
            yield scrapy.Request(url=url, callback=self.parse)

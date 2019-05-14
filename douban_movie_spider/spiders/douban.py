# -*- coding: utf-8 -*-
import scrapy
from douban_movie_spider.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        for item in response.css('div.item'):
            movie = MovieItem()
            rank = item.css('div.pic em::text').extract_first()
            title = item.css('div.info div.hd span.title::text').extract_first()
            star = item.css('div.star span.rating_num::text').extract_first()
            quote = item.css('p.quote span.inq::text').extract_first()
            movie['rank'] = rank
            movie['title'] = title
            movie['star'] = star
            movie['quote'] = quote
            yield movie

        # 获取下一页的url
        next_url = response.css('span.next a::attr("href")').extract_first()
        if next_url is not None:
            url = self.start_urls[0] + next_url
            yield scrapy.Request(url=url, callback=self.parse)

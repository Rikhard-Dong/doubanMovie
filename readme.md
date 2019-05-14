# 豆瓣电影 TOP250
> 使用scrapy爬取[豆瓣电影top250](https://movie.douban.com/top250)

## 创建项目
首先在终端使用scrapy startproject 命令创建scrapy创建spider项目
```
scrapy startproject douban_movie_spider
```
项目创建完成后可以使用pycharm等ide打开项目

## 实现爬虫
### 设置UA
在settings.py中可以设置ua, 代码如下

```python
# 设置UA
import random
USER_AGENT_LIST = [
    'MSIE (MSIE 6.0; X11; Linux; i686) Opera 7.23',
    'Opera/9.20 (Macintosh; Intel Mac OS X; U; en)',
    'Opera/9.0 (Macintosh; PPC Mac OS X; U; en)',
    'iTunes/9.0.3 (Macintosh; U; Intel Mac OS X 10_6_2; en-ca)',
    'Mozilla/4.76 [en_jp] (X11; U; SunOS 5.8    sun4u)',
    'iTunes/4.2 (Macintosh; U; PPC Mac OS X 10.2)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0) Gecko/20100101 Firefox/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0) Gecko/20100101 Firefox/9.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:16.0) Gecko/20120813 Firefox/16.0',
    'Mozilla/4.77 [en] (X11; I; IRIX;64 6.5 IP30)',
    'Mozilla/4.8 [en] (X11; U; SunOS; 5.7 sun4u)'
]
USER_AGENT = random.choice(USER_AGENT_LIST)
```
这里使用了一个ua list, 随机选取一个ua, 也可以直接赋一个固定的值

### 编写item
在items.py中编写一个item用于存放爬取结果
```python
import scrapy


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    star = scrapy.Field()
    rank = scrapy.Field()
    quote = scrapy.Field()
```
### 编写爬取类
创建一个豆瓣电影的spider类, 继承自scrapy.Spider类
```python

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
            star = item.css('duv.star span.rating_num::text').extract_first()
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
```
通过对网页源代码的分析, 我们发现我们所要获取的信息都在class为item中的div中, 遍历这些div,
获取相关数据.

每一页有有25部电影数据, 当这一页的数据获取完成后, 接着爬取下一页的数据.

另外也可以通过xpath解析网页.

### 运行爬虫
在terminal中输入**scrapy crawl douban**, 执行

### 将爬取的信息保存到文件
```
scrapy crawl douban -o top250.json -s FEED_EXPORT_ENCODING=UTF-8
```

## 更加优雅的保存数据方式
前面提到了使用-o直接将结果输出到文件中, 其实利用pipeline可以更优雅的实现数据的保存

### 编写pipeline类, 将数据保存到文件中
参考pipelines.py中的SaveFilePipeline类, 实现了几个方法
1. __init__()方法

    初始化一些参数, 比如可以在这里打开文件或者打开数据库连接, 不过也可以在oen_spider中进行这些操作

2. open_spider()方法
    
    同上    
   
3. process_item()方法

    处理爬取到的item, 如果只有一个pipeline, 则可以不用return item, 如果有多个pipeline的话, 则需要return, 否则优先度低的pipeline获取到item为None, 会报错.
    简单来说就是一个流水线操作, 如果上流断流了, 下流就没有数据了
    
4. close_spider()方法
    
    爬取结束, 可以关闭文件或者数据库连接等.
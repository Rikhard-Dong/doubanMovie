# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs


# 将爬取的内容保存到文件中
class SaveFilePipeline(object):

    def __init__(self) -> None:
        print("======== 将爬取结果保存到文件中 =======")
        self.res_list = []
        super().__init__()

    def process_item(self, item, spider):
        res = dict(item)
        # print(str)
        self.res_list.append(res)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        print("====== 爬取结束 ======")
        # print(self.res_list)
        # 打开文件, w+ 读写, 如果文件不存在会被创建, 存在则内容会被清空会重写写入
        file = codecs.open(filename="douban_movie_top_250.json", mode='w+', encoding='utf-8')
        # ensure_ascii=False 保证输出的是中文而不是unicode字符
        file.write(json.dumps(self.res_list, ensure_ascii=False))
        file.close()


# 将爬取的内容保存到mongoDB中
class Save2MongoPipeline(object):

    def __init__(self) -> None:
        super().__init__()
        print("======== 将爬取结果保存到MongoDB中 =======")

    def process_item(self, item, spider):
        return item

# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SaveFilePipeline(object):

    def __init__(self) -> None:
        print("======== 将爬取结果保存到文件中 =======")
        super().__init__()

    def process_item(self, item, spider):
        print(item)
        return item

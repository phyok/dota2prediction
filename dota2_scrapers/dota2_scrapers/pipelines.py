from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class Dota2ScrapersPipeline(object):
    def process_item(self, item, spider):
        return item

def item_type(item):
    return type(item).__name__.lower()

class DotabuffCsvItemPipeline(object):
    def __init__(self):
        self.item_types = ['hero', 'player']

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.files = dict([(item_type, open('%s_%s.csv' % (spider.name, item_type), 'w+b')) for item_type in self.item_types])
        self.exporters = dict([(item_type, CsvItemExporter(self.files[item_type])) for item_type in self.item_types])
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        t = item_type(item)
        if t in self.item_types:
            self.exporters[t].export_item(item)
        return item

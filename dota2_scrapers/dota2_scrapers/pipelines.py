from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.conf import settings
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class Dota2ScrapersPipeline(object):
    def process_item(self, item, spider):
        return item

class DatDotaCsvItemPipeline(object):

    match_export_fields = [
        'match_id',
        'radiant_team',
        'dire_team',
        'winner',
        'radiant_player_0',
        'radiant_player_1',
        'radiant_player_2',
        'radiant_player_3',
        'radiant_player_4',
        'radiant_hero_0',
        'radiant_hero_1',
        'radiant_hero_2',
        'radiant_hero_3',
        'radiant_hero_4',
        'dire_player_0',
        'dire_player_1',
        'dire_player_2',
        'dire_player_3',
        'dire_player_4',
        'dire_hero_0',
        'dire_hero_1',
        'dire_hero_2',
        'dire_hero_3',
        'dire_hero_4'
        ]

    player_export_fields = [
        'player',
        'matches',
        'wins',
        'losses',
        'win_rate'
        ]

    hero_export_fields = [
        'hero',
        'matches',
        'wins',
        'losses',
        'win_rate'
        ]

    hero_mapper_export_fields = [
        'hero_alt',
        'hero'
        ]

    def __init__(self):
        self.files = {}
        self.exporters = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open('%s.csv' % spider.name, 'w')
        self.files[spider.name] = file
        exporter = CsvItemExporter(file)
        if spider.name == 'datdota_matches':
            exporter.fields_to_export = DatDotaCsvItemPipeline.match_export_fields
        elif spider.name == 'datdota_players':

            exporter.fields_to_export = DatDotaCsvItemPipeline.player_export_fields
        elif spider.name == 'datdota_heroes':
            exporter.fields_to_export = DatDotaCsvItemPipeline.hero_export_fields
        elif spider.name == 'datdota_hero_mapper':
            exporter.fields_to_export = DatDotaCsvItemPipeline.hero_mapper_export_fields
        self.exporters[spider.name] = exporter
        exporter.start_exporting()

    def spider_closed(self, spider):
        exporter = self.exporters.pop(spider.name)
        exporter.finish_exporting()
        file = self.files.pop(spider.name)
        file.close()

    def process_item(self, item, spider):
        self.exporters[spider.name].export_item(item)
        export_fields = None
        if spider.name == 'datdota_matches':
            export_fields = DatDotaCsvItemPipeline.match_export_fields
        elif spider.name == 'datdota_players':
            export_fields = DatDotaCsvItemPipeline.player_export_fields
        elif spider.name == 'datdota_heroes':
            export_fields = DatDotaCsvItemPipeline.hero_export_fields
        elif spider.name == 'datdota_hero_mapper':
            export_fields = DatDotaCsvItemPipeline.hero_mapper_export_fields
        if export_fields:
            for field in export_fields:
                if not item.get(field, None):
                    raise DropItem('Missing %s in %s' % (field, item))
            if spider.name == 'datdota_hero_mapper' or item.update():
                return item

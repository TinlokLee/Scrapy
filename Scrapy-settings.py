# -*- coding: utf-8 -*-

BOT_NAME = 'Sina'
SPIDER_MODULES = ['Sina.spiders']
NEWSPIDER_MOUDLE = 'Sina.spiders'

ITEM_PIPELINES = {
    'Sina.pipelines.SinaPipeline': 500,
}

LOG_LEVEL = 'DEBUG'

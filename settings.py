BOT_NAME = 'Sina'

SPIDER_MODULES = ['Sina.spiders']
NEWSPIDER_MODULE = 'Sina.spiders'

ITEM_PIPELINES = {
'Sina.pipelines.SinaPipeline': 300,
}

LOG_LEVEL = 'DEBUG'
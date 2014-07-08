# Scrapy settings for profcrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'profcrawl'

SPIDER_MODULES = ['profcrawl.spiders']
NEWSPIDER_MODULE = 'profcrawl.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'profcrawl (+http://www.yourdomain.com)'

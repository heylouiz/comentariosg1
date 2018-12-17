# -*- coding: utf-8 -*-
from user_agent import generate_user_agent

BOT_NAME = 'comentariosg1'

SPIDER_MODULES = ['comentariosg1.spiders']
NEWSPIDER_MODULE = 'comentariosg1.spiders'


USER_AGENT = generate_user_agent(device_type=['desktop'])

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

FEED_EXPORT_ENCODING = 'utf-8'

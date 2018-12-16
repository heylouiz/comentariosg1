# -*- coding: utf-8 -*-
import json
import re
import scrapy

from scrapy.loader import ItemLoader
from comentariosg1.items import Comentariosg1Item


class G1commentsSpider(scrapy.Spider):
    name = 'g1comments'
    start_urls = ['https://g1.globo.com/']
    comment_api_url = 'https://comentarios.globo.com/comentarios/{uri}/{external_id}/{url}/shorturl/{title}/1.json'

    def parse(self, response):
        for category in response.xpath('//li[@id="menu-1-editorias"]/ul/li/a[1]/@href'):
            yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response):
        items = response.xpath('//script[contains(text(),"RenderFunction")]').re_first(r'("items":\[.*\])')
        items = json.loads('{%s}' % items)
        items = items['items']

        for news in items:
            url = news['content']['url']
            yield response.follow(url, callback=self.parse_news)

    def parse_news(self, response):
        uri = response.xpath('//script').re_first(r'COMENTARIOS_URI: "(.*?)",')
        external_id = response.xpath('//script').re_first(r'COMENTARIOS_IDEXTERNO: "(.*?)",')
        title = response.xpath('//script').re_first(r'TITLE: "(.*?)",')

        if not uri or not external_id or not title:
            return None

        return response.follow(
                self.comment_api_url.format(uri=uri.replace('/', '@@'),
                                            external_id=external_id.replace('/', '@@'),
                                            url=response.url.replace('/', '@@'),
                                            title=title),
                callback=self.parse_comments
                )

    def parse_comments(self, response):
        items = re.search(r'("itens":\[.*\])', response.text)
        if not items:
            return None
        comments = json.loads('{%s}' % items.group(1))['itens']
        for comment in comments:
            for reply in comment['replies']:
                yield self.extract_comment(reply)
            yield self.extract_comment(comment)

    def extract_comment(self, comment):
        il = ItemLoader(item=Comentariosg1Item())
        il.add_value('id', comment['idComentario'])
        il.add_value('user_id', comment['Usuario']['usuarioId'])
        il.add_value('user_name', comment['Usuario']['nome'])
        il.add_value('user_img_url', comment['Usuario']['avatarImgUrl'])
        il.add_value('user_oficial', comment['Usuario']['usuarioOficial'])
        il.add_value('thumb_up', comment['VotosThumbsUp'])
        il.add_value('thumb_down', comment['VotosThumbsDown'])
        il.add_value('text', comment['texto'])
        il.add_value('facebook_id', comment['facebook_id'])
        for reply in comment.get('replies', []):
            il.add_value('replies', reply['idComentario'])
        il.add_value('original_date', comment['dataRFC1123'])
        il.add_value('last_edit_date', comment.get('data_ultima_atualizacao'))
        il.add_value('news_url', comment['topico']['url'])
        il.add_value('news_title', comment['topico']['titulo'])
        return il.load_item()

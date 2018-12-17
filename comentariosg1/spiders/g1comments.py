# -*- coding: utf-8 -*-
import json
import re
import scrapy

from comentariosg1.items import Comentariosg1ItemLoader


class G1commentsSpider(scrapy.Spider):
    name = 'g1comments'
    start_urls = ['https://g1.globo.com/']
    comment_api_url = 'https://comentarios.globo.com/comentarios/{uri}/{external_id}/{url}/shorturl/{title}/{page}.json'
    next_page_url = 'https://falkor-cda.bastian.globo.com/tenants/g1/instances/{id}/posts/page/{page}'
    votes_count_url = 'https://interatividade.globo.com/notas/agregador/{id}/resultado-resumido.jsonp'
    max_pages = 10

    def start_requests(self):
        if hasattr(self, 'max_pages'):
            self.max_pages = int(self.max_pages)

        if hasattr(self, 'category_url'):
            yield scrapy.Request(self.category_url, callback=self.parse_category)
        elif hasattr(self, 'news_url'):
            yield scrapy.Request(self.news_url, callback=self.parse_news)
        else:
            for url in self.start_urls:
                yield scrapy.Request(url)

    def parse(self, response):
        for category in response.xpath('//li[@id="menu-1-editorias"]/ul/li/a[1]/@href'):
            yield response.follow(category, callback=self.parse_category)

    def parse_category(self, response):
        if response.meta.get('is_json'):
            config = json.loads(response.text)
        else:
            config = response.xpath('//script[contains(text(),"RenderFunction")]').re_first(r'({"config":{.*})\);')
            config = json.loads(config)
        items = config['items']
        id = config['id']
        next_page = config['nextPage']

        for news in items:
            url = news['content']['url']
            yield response.follow(url, callback=self.parse_news)

        if next_page <= self.max_pages:
            yield response.follow(self.next_page_url.format(id=id, page=next_page),
                                  callback=self.parse_category, meta={'is_json': True})

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
                                            title=title,
                                            page=1),
                callback=self.parse_comments
                )

    def parse_comments(self, response):
        data = re.search(r'__callback_listacomentarios\((.*)\)', response.text)
        if not data:
            return None
        data = json.loads(data.group(1))
        comments = data['itens']
        aggregator = data['agregador']
        if not comments:
            return
        for comment in comments:
            for reply in comment['replies']:
                yield self.extract_comment(reply, aggregator)
            yield self.extract_comment(comment, aggregator)
        next_page = int((data['fim'] / data['itensPorPagina']) + 1)
        yield response.follow(re.sub(r'\d+.json', f'{next_page}.json', response.url), callback=self.parse_comments)

    def extract_comment(self, comment, aggregator):
        il = Comentariosg1ItemLoader()
        il.add_value('id', comment['idComentario'])
        il.add_value('user_id', comment['Usuario']['usuarioId'])
        il.add_value('user_name', comment['Usuario']['nome'])
        il.add_value('user_img_url', comment['Usuario']['avatarImgUrl'])
        il.add_value('user_oficial', comment['Usuario']['usuarioOficial'])
        il.add_value('thumb_up_id', comment['idThumbsUp'])
        il.add_value('thumb_down_id', comment['idThumbsDown'])
        il.add_value('interaction_id', comment['idInteratividade'])
        il.add_value('text', comment['texto'])
        il.add_value('facebook_id', comment['facebook_id'])
        for reply in comment.get('replies', []):
            il.add_value('replies', reply['idComentario'])
        il.add_value('original_date', comment['dataRFC1123'])
        il.add_value('last_edit_date', comment.get('data_ultima_atualizacao'))
        il.add_value('news_url', comment['topico']['url'])
        il.add_value('news_title', comment['topico']['titulo'])
        il.add_value('aggregator_url', self.votes_count_url.format(id=aggregator))
        return il.load_item()

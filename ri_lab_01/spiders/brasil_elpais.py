# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []]
    data_limit = datetime.strptime('01/01/2018', '%d/%m/%Y')


    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        for notice in response.css("div.articulo__envoltorio"):
            yield{
                "title": notice.css("h1.articulo-titulo::text").get(),
                "subtitle": notice.css("h2.articulo-subtitulo::text").get(),
                "author": notice.css("span.autor-nombre a::text").get()
            }
        for notice_url in response.css("figure.foto a::attr(href)").getall():
            if notice_url is not None:
                    yield scrapy.Request(notice_url, callback=self.parse)
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

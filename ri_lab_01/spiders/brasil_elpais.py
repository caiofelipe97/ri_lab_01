# -*- coding: utf-8 -*-
import scrapy
import json

from ri_lab_01.items import RiLab01Item
from ri_lab_01.items import RiLab01CommentItem
from datetime import datetime


class BrasilElpaisSpider(scrapy.Spider):
    name = 'brasil_elpais'
    allowed_domains = ['brasil.elpais.com']
    start_urls = []
    data_limit = datetime.strptime('01/01/2018', '%d/%m/%Y')


    def __init__(self, *a, **kw):
        super(BrasilElpaisSpider, self).__init__(*a, **kw)
        with open('seeds/brasil_elpais.json') as json_file:
                data = json.load(json_file)
        self.start_urls = list(data.values())

    def parse(self, response):
        for notice in response.css("div.articulo__envoltorio"):
            texts = response.css('div.articulo__contenedor p::text').getall()
            notice_text = ''
            for text in texts:
                notice_text += text.replace("\n", "")

            data = notice.css('time::attr(datetime)').get()
            editedData = datetime.strptime(data[:-6], '%Y-%m-%dT%H:%M:%S')
            if(editedData >= self.data_limit):
                yield{
                    "title": notice.css("h1.articulo-titulo ::text").get(),
                    "subtitle": notice.css("h2.articulo-subtitulo::text").get(),
                    "author": notice.css("span.autor-nombre a::text").get(),
                    "section": notice.css("div.seccion a.enlace span::text").get(),
                    "data":   editedData,
                    "text":   notice_text,
                    "url":    response.url
                }
        for notice_url in response.css("figure.foto a::attr(href)").getall():
            if notice_url is not None:
                yield scrapy.Request("https:" + notice_url, callback=self.parse)
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

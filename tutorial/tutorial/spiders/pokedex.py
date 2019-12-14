# -*- coding: utf-8 -*-
import scrapy


class PokedexSpider(scrapy.Spider):
    name = 'pokedex'
    allowed_domains = ['pokemon.com']
    start_urls = ['https://www.pokemon.com/uk/pokedex/bulbasaur']

    def parse(self, response):
        filename = 'bulbasaur.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
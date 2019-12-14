# -*- coding: utf-8 -*-
import scrapy

from tutorial.items import PokemonItem


class PokedexSpider(scrapy.Spider):
    name = 'pokedex'
    allowed_domains = ['pokemon.com']
    start_urls = ['https://www.pokemon.com/uk/pokedex/bulbasaur']

    def parse(self, response):
        #Podemos guardar un fichero concreto en nuestro disco para analizar los campos
        filename = 'bulbasaur.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        #Modificamos nuestro spider para que almacene la información en el item que acabamos de crear:
        pokemon = PokemonItem()
        pokemon['id'] = response.css('div.pokedex-pokemon-pagination-title div span::text').re_first('[0-9]{3}')
        pokemon['name'] = response.css('div.pokedex-pokemon-pagination-title div::text').extract_first().strip()
        pokemon['description'] = response.css('div.version-descriptions p.active::text').extract_first().strip()
        pokemon['evolution'] = response.css('section.pokedex-pokemon-evolution li span::text').extract()
        pokemon['type'] = response.css('div.pokedex-pokemon-attributes div.dtm-type ul')[0].css("li a::text").extract()
        pokemon['height'] = response.css('div.pokemon-ability-info ul li')[0]\
                                .css("span.attribute-value::text").re_first(r'\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")
        pokemon['weight'] = response.css('div.pokemon-ability-info ul li')[1]\
                                .css("span.attribute-value::text").re_first(r'\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")

        yield pokemon
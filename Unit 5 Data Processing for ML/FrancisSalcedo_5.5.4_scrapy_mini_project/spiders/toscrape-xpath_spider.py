import scrapy

class ToScrapeXpathSpider(scrapy.Spider):
    name = 'xpath-scraper-results.json'

    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # author_page_links = response.css('.author + a')
        author_page_links = response.xpath('//*[contains(concat(" ", @class, " "), " author ")]/following-sibling::a[1]')
        yield from response.follow_all(author_page_links, self.parse_author)
        
        # pagination_links = response.css('li.next a')
        pagination_links = response.xpath('//li[contains(concat(" ", @class, " "), " next ")]//a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_author(self, response):
        #def extract_with_css(query):
        #    return response.css(query).get(default='').strip()
        
        def extract_with_xpath(query):
            return response.xpath(query).get(default='').strip()
        
        # 'h3.author-title::text'
        # .author-born-date::text'
        # .author-description::text'
        # text()[1]
        
        # //h3[contains(concat(" ", @class, " "), " author-title ")]/text()
        # //*[contains(concat(" ", @class, " "), " author-born-date ")]/text()
        # //*[contains(concat(" ", @class, " "), " author-description ")]/text()
        
        yield {
            'name': extract_with_xpath('//h3[contains(concat(" ", @class, " "), " author-title ")]/text()'),
            'birthdate': extract_with_xpath('//*[contains(concat(" ", @class, " "), " author-born-date ")]/text()'),
            'bio': extract_with_xpath('//*[contains(concat(" ", @class, " "), " author-description ")]/text()'),
        }
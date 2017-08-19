import scrapy
import os

class BashSpider(scrapy.Spider):
    name = 'ipfs-spider'
    start_urls = ['http://bash.org/?browse&p=1']

    def parse(self, response):
        quotes = zip(
            response.xpath('//p[@class="quote"]'),
            response.xpath('//p[@class="qt"]')
        )

        if not os.path.exists('bash.org'):
            os.makedirs('bash.org')

        for x, q in quotes:
            id = x.xpath('./a/@href').extract_first().strip('?')
            id = int(id)

            quote = q.xpath('string(.)').extract_first()
            quote = quote.replace('\r\n', '\n')

            with open('bash.org/%d.txt' % id, 'w') as f:
                f.write('%s\n' % quote)

            yield {'x': (id, quote)}

        for a in response.xpath('//a[@class="qa"]'):
            if a.xpath('string(.)').extract_first() == '>':
                next = a.xpath('./@href').extract_first()
                yield scrapy.Request(response.urljoin(next))
                break

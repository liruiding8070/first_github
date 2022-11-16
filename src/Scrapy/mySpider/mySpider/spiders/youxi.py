import scrapy

from mySpider.items import MyspiderItem


class YouxiSpider(scrapy.Spider):
    name = 'youxi'
    allowed_domains = ['4399.com']
    start_urls = ['http://www.4399.com/flash/']

    def parse(self, response, **kwargs):
        li_list = response.xpath("//ul[@class='n-game cf']/li")
        for li in li_list:
            name = li.xpath("./a/b/text()").extract_first()
            category = li.xpath("./em/a/text()").extract_first()
            date = li.xpath("./em/text()").extract_first()

            dic = {
                "name": name,
                "category": category,
                "date": date
            }
            item = MyspiderItem()
            item["name"] = name
            item["category"] = category
            item["date"] = date
            yield item

            # yield dic

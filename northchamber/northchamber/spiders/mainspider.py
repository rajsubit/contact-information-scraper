import scrapy

from ..items import NorthchamberItem


class NorthChamberSpider(scrapy.Spider):

    name = "north_chamber"
    start_urls = ["http://www.northchamber.co.nz/all-members/", ]

    def parse(self, response):
        for href in response.xpath("//h3/a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_content)

    def parse_dir_content(self, response):
        item = NorthchamberItem()
        member_name = response.xpath(
            "//div[@class='page-header']/h1/text()").extract_first()
        if member_name:
            item['member_name'] = member_name.strip()
        website = response.xpath(
            "//div[@class='col-sm-12']/a/text()").extract_first()
        if website:
            item['website'] = website.strip()
        title_list = response.xpath(
            "//div[@class='col-sm-12']/strong/text()").extract()
        text_extract = response.xpath(
            "//div[@class='col-sm-12']/text()").extract()
        text_list = [t.strip() for t in text_extract]
        text_list = filter(None, text_list)
        if 'Phone:' in title_list:
            item['phone'] = text_list[0]
            text_list.pop(0)
        if 'Mobile:' in title_list:
            item['mobile'] = text_list[0]
            text_list.pop(0)
        if 'Address:' in title_list:
            item['address'] = text_list[0]
        yield item

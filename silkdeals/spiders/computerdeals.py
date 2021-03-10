# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest


class ComputerdealsSpider(scrapy.Spider):
    name = 'computerdeals'
    url = "https://slickdeals.net/computer-deals/"
    
    def remove_characters(self, value):
        return value.strip('\xa0')

    def start_requests(self):
        yield SeleniumRequest(
            url=self.url,
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals']/li")
        for product in products:
            yield {
                'name': product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/text()").get(),
                'link': product.xpath(".//a[@class='itemTitle bp-p-dealLink bp-c-link']/@href").get(),
                'store_name': self.remove_characters(product.xpath("normalize-space(.//button[contains(@class,'itemStore')]/text())").get()),
                'price': product.xpath("normalize-space(.//div[contains(@class,'itemPrice')]/text())").get(),
            }
        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
            url=absolute_url,
            wait_time=3,
            callback=self.parse
        )
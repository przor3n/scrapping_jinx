# -*- coding: utf-8 -*-
from zeug.pages import ScrapyPage


class Euler(ScrapyPage):
    start_urls = ['https://projecteuler.net/archives']
    keywords_xpath = '//meta[@name="keywords"]/@content'
    title_xpath = '//h2/text()'

    list_link_to_content_xpath = '//table[@id="problems_table"]//a/@href'
    list_pagination_links_xpath = '//*[@class="pagination noprint"]//a/@href'

    article_page = '//*[@class="problem_content"]'

    extraction = {
        'title': '//h2/text()',
        'content': '//*[@class="problem_content"]/text()'
    }

    def content_links(self, response):
        for href in response.xpath(self.list_link_to_content_xpath).getall():
            yield response.urljoin(href)

    def list_pagination_links(self, response):
        for href in response.xpath(self.list_link_to_content_xpath).getall():
            yield response.urljoin(href)
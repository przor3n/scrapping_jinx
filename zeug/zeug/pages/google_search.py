from zeug.pages import ScrapyPage


class GoogleSearch(ScrapyPage):
    start_urls = ['https://www.wykop.pl/sitemap.xml']
    is_single = False  # links in start_urls are list pages
    is_xml = True

    keywords_xpath = ''
    title_xpath = ''
    list_link_to_content_xpath = '//div[@class="r"]//a/@href'
    pagination_links_xpath = '//td/a[@class="fl"]/@href'
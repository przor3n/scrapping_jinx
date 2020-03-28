from wykoppl.pages import ScrapyPage


class WykopXML(ScrapyPage):
    start_urls = ['https://www.wykop.pl/sitemap.xml']
    is_single = False  # links in start_urls are list pages
    is_xml = True

    keywords_xpath = ''
    title_xpath = ''
    list_link_to_content_xpath = '//url/loc/text()'
    pagination_links_xpath = '//loc/text()'


class Wykop(WykopXML):
    is_single = True
    is_xml = False

    list_link_to_content_xpath = ''
    pagination_links_xpath = ''
    content_pagination_links_xpath = '//a[@class="button"]/@href'
    publish_date_xpath = "//div[@class='space information bdivider']/div/p/b/*[@itemprop='datePublished']"

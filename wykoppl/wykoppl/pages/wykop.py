import dateutil.parser as dp


class Wykop:
    publish_date_xpath = "//div[@class='space information bdivider']/div/p/b/*[@itemprop='datePublished']"
    next_pages_xpath = '//a[@class="button"]/@href'
    sitemap_url = 'https://www.wykop.pl/sitemap.xml'
    first_tier_sitemaps_xpath = '//loc/text()'
    second_tier_links_xpath = '//url/loc/text()'

    @staticmethod
    def publish_date(response):
        try:
            datetime_string = response.xpath(Wykop.publish_date_xpath).attrib['datetime']
        except KeyError:
            datetime_string = '1985-04-25T15:35:33.171002'  # if something was published on my birthday, then something went wrong Marty. We must have left somehting in the past.

        return dp.parse(datetime_string)
    
    @staticmethod
    def next_pages(response):
        return response.xpath(Wykop.next_pages_xpath).getall()
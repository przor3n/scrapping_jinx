import dateutil.parser as dp
import os
import importlib.util


def get_page_object(_module, _class):  # TO PIERDOLNIE
    """Import the _module and return instance of _class"""
    from _module import _class as c
    return c()

    p = os.path.abspath(os.path.dirname(__file__))
    module_path = os.path.join(p, _module + '.py')

    # importlib.util.find_spec(name, package=None)
    spec = importlib.util.spec_from_file_location("zeug.pages." + _module,
                                                  module_path)
    _mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_mod)
    c = getattr(_mod, _class)()

    return c


class ScrapyPage:
    start_urls = []  # list of URLS to crawl/download

    is_single = False  # links in start_urls are list pages

    is_xml = False  # if is_xml the response.selector.remove_namespaces() will be done

    """Below are selectors, all in XPATH. """

    # path for keywords/tags
    keywords_xpath = ''

    # path for title extraction
    title_xpath = ''

    # path to content links
    # .i.e. links to content, recent posts, other similar
    list_link_to_content_xpath = ''

    # path for pagination of list of links
    # i.e. category pages are alfabetical
    list_pagination_links_xpath = ''

    # path for
    # a list of links to pages with listed content
    # i.e. links to book category pages, that display list of books under that category
    list_links_xpath = ''

    # path for pagination on content page
    # i.e. pagination for post comments
    content_pagination_links_xpath = ''

    # path for publish date
    publish_date_xpath = ''

    def publish_date(self, response):
        try:
            datetime_string = response.xpath(
                self.publish_date_xpath).attrib['datetime']
        except KeyError:
            datetime_string = '1985-04-25T15:35:33.171002'  # if something was published on my birthday, then something went wrong Marty. We must have left somehting in the past.

        return dp.parse(datetime_string)

    def tags(self, response):
        return response.xpath(self.keywords_xpath).get()

    def title(self, response):
        return response.xpath(self.title_xpath).get()

    def content_links(self, response):
        return response.xpath(self.list_link_to_content_xpath).getall()

    def list_links(self, response):
        return response.xpath(self.list_links_xpath).getall()

    def content_pagination_links(self, response):
        return response.xpath(self.content_pagination_links_xpath).getall()

    def list_pagination_links(self, response):
        return response.xpath(self.list_pagination_links_xpath).getall()

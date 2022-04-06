import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from django.db import models
import json

from src.posts.models import PostGame


class ParseUrl(models.Model):
    """ Класс содержит в себе сайты и их селекторы, по которым надо пропарсить сайт.
        Модель для администратора Games Klondike.
    """
    SiteName = models.CharField(max_length=255, unique=True)
    SiteURL = models.URLField()
    SubPageURL = models.URLField(blank=True, null=True)
    NextPageUrl = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = 'Parse URL'
        verbose_name_plural = 'Parse URL'

    def __str__(self) -> str:
        return f'{self.SiteName}'


class PageSelector(models.Model):
    UrlID = models.ForeignKey(
        ParseUrl, on_delete=models.CASCADE, related_name='page_selector')

    Selector = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Page selector'
        verbose_name_plural = 'Page selector'

    def __str__(self) -> str:
        return f'{self.UrlID} ### {self.Selector}'


class SubpageSelector(models.Model):
    UrlID = models.ForeignKey(
        ParseUrl, on_delete=models.CASCADE, related_name='subpage_selector')

    Selector = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Page selector'
        verbose_name_plural = 'Page selector'

    def __str__(self) -> str:
        return f'{self.UrlID} ### {self.Selector}'


####################################################################################################
# Custom models for parser
####################################################################################################
class Page:
    """ Содержит элементы и ошибки с проппаршеной странцы
    """
    __slots__ = ('_Page__error', '_Page__url',
                 '_Page__soup', '_Page__selectors',
                 '_Page__all_tags', '_Page__subpage_selectors')

    def __init__(self, url, soup, selectors=None, subpage_selectors=False):
        self.__error = ''
        self.__url = ''
        self.__selectors = selectors
        self.__subpage_selectors = subpage_selectors
        self.__soup = soup
        self.__all_tags = tuple([])
        if isinstance(url, (str)):
            if self.check_site(url):
                self.__url = url
            else:
                self.__error = 'This site does not open'
        else:
            self.__error = 'url is not string'
        # Creating and sorting empty lists
        try:
            self.__set_all_tags()
        except:
            self.__error = 'Incorrect data type '

    def __set_all_tags(self):
        """
                {
                    'selector': 'selector',
                    'tags': [] 
                }
        """
        if self.__selectors == None:
            self.__error = str('Exception: Slectors are not selected')
            print(f'\r\nSTART: {self.__error}\r\n')
            self.__all_tags = tuple([{
                'selector': None,
                'tags': [self.__create_HtmlItem(item=tag)
                         for tag in self.__soup.find_all()]
            }])
            print(f'\r\n END: {self.__error}\r\n')
        else:
            if self.__subpage_selectors:
                """ Если парсится подстраница:
                """
                try:
                    self.__all_tags = {
                        'Title': self.__soup.select(
                            self.__selectors['Title_selector'])[0].text.strip()
                        if len(self.__soup.select(self.__selectors['Title_selector'])) > 0
                        else None,

                        'Description': self.__soup.select(
                            self.__selectors['Description_selector'])[0].text.strip()
                        if len(self.__soup.select(self.__selectors['Description_selector'])) > 0
                        else None,

                        'Reliase date': self.__soup.select(self.__selectors['Reliase_date_selector'])[0].text.strip()
                        if len(self.__soup.select(self.__selectors['Reliase_date_selector'])) > 0
                        else None,

                        'Tags':  [tag.text.strip()
                                  for tag in self.__soup.select(self.__selectors['Tags_selector'])],
                        'Images': [tag['src']
                                   for tag in self.__soup.select(self.__selectors['img_selector'])],
                    }
                except Exception as ex:
                    print(f'Exception: {ex}')
                print(f'aaaaaaaaaaaaaaaaaaaaaa\r\n{self.__all_tags}\r\n')
            else:
                self.__all_tags = list(filter(None, self.__soup))
                # print(self.__elements)
                self.__all_tags = tuple([{
                    'selector': selector,
                    'tags': [self.__create_HtmlItem(item=tag)
                             for tag in list(dict.fromkeys(self.__soup.select(selector)))]
                } for selector in self.__selectors])

    def print_error(self):
        print(self.__error)
        return self.__error

    def get_dict(self):
        # print([[j.get_dict() for j in i] for i in self.__elements])
        return {
            'url': self.__url,
            'all_tags_from_page': self.__all_tags,
            'error': self.__error
        }

    def check_site(self, site_name):
        try:
            requests.get(site_name)
            return True
        except:
            self.__error = 'Unknown site'
            return False

    def __create_HtmlItem(self, item):
        root = ET.fromstring(str(item))

        # print(f'\r\n Create: {root}\r\n')
        return {
            'tag': root.tag,
            'text': root.text,
            'atribs': root.attrib
        }


class Parser:
    """ Парсер
        Запуск:
        1) Создать класс
        2) Применить метод parse()
        3) Желательно работать с JSON форматом, т.к так проще (метод get_JSON())
    """
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def __init__(self, site_url=None, selector_link_to_subpage=None, multipage=None, subpage_selectors=None, number_of_readable_pages=1000000):
        self.__error = ''
        if self.check_site(site_url):
            self.__site_url = site_url
        else:
            self.__site_url = None
        self.__multipage = multipage

        self.__req = None
        self.__pages = []
        self.__there_is_the_following_page = True
        self.__counter = number_of_readable_pages
        self.__all_urls = []

        self.__selector_link_to_subpage = selector_link_to_subpage
        if isinstance(self.__selector_link_to_subpage, (list, tuple)):
            for el in self.__selector_link_to_subpage:
                if not isinstance(el, str):
                    self.__selector_link_to_subpage = None
                    break
        else:
            self.__selector_link_to_subpage = None

        if self.__multipage == '' or not isinstance(self.__multipage, str):
            self.__multipage = None

        self.__subpage_selectors = subpage_selectors

    def check_site(self, site_name):
        try:
            requests.get(site_name)
            return True
        except:
            self.__error = 'Unknown site'
            return False

    def print_error(self):
        print(self.__error)
        return self.__error

    def parse(self):
        if self.__site_url == None:
            return tuple([])
        self.__req = self.__get_request(url=self.__site_url)
        try:
            counter = 1
            while self.__there_is_the_following_page and counter < self.__counter:
                print(counter)
                self.__error = ''
                self.__there_is_the_following_page = False
                if self.__site_url == None:
                    self.__error = 'Site url is None (may be all\'re Ok)'
                    break

                if self.__req.status_code != 200:
                    self.__error = str(f'Exception: {self.__req}')
                    break
                # print('self.__site_url\t',self.__site_url)

                soup = BeautifulSoup(self.__req.text, 'html.parser')

                self.__pages.append(
                    Page(url=self.__site_url,
                         #  elements=[                                                          #уже не elements, а soup
                         #      [self.__create_HtmlItem(item=item) for item in soup.select(
                         #          selector)]    # foreach in soup items
                         #      for selector in self.__selectors]  # foreach in selectors
                         soup=soup,
                         selectors=self.__selector_link_to_subpage
                         )
                )
                if self.__multipage != None:
                    url_list = soup.select(self.__multipage)
                    if url_list != []:
                        # print(self.__site_url, soup.select(self.__multipage))
                        self.__check_url_for_next_page(
                            urljoin(self.__site_url, url_list[-1].get('href')))

                # print(counter, self.__all_urls)

                counter += 1
        except Exception as e:
            self.__error = e
            print(e)

        self.subpage_urls = self.__get_subpage_urls_from_pages()
        return tuple(self.__pages)

    def __check_url_for_next_page(self, url):
        # print('THIS URL\t', urljoin(self.__site_url, url))
        try:    # Check on the site link (with or without domain)
            self.__get_request(url)
            self.__site_url = url
            if self.__site_url not in self.__all_urls:
                self.__all_urls.append(self.__site_url)
                self.__there_is_the_following_page = True
        except:
            self.__error = '''__check_url_for_next_page() return except (pages maybe they ended)'''

    def __get_request(self, url, params=None):
        req = requests.get(
            url, headers=self.HEADERS, params=params)
        self.__req = req
        self.site_url = url
        return self.__req
        # print(self.__req)

    def get_JSON(self, sort_keys=False, indent=None) -> json:
        """ Принимает список с объектами класса Page
        """
        # if not isinstance(pages, (tuple, list)) or not [isinstance(page, Page) for page in pages]:
        #     raise TypeError
        return json.dumps(Parser().get_dict(self.__pages), sort_keys=sort_keys, indent=indent)

    @staticmethod
    def get_dict(pages):
        """ Принимает список с объектами класса Page и отдаёт словарь
        """
        return [el.get_dict() for el in pages]

    def get_all_keys_and_values_from_pages(self):
        """ Запись данных в БД
        """
        for page in Parser.get_dict(self.__pages):
            page['url']
            page['error']
            for all_tags in page['all_tags_from_page']:
                all_tags['selector']
                for tag_by_selector in all_tags['tags']:
                    tag_by_selector['tag']
                    tag_by_selector['text']
                    for atrib_key, atrib_value in tag_by_selector['atribs'].items():
                        atrib_key
                        atrib_value

    def __get_subpage_urls_from_pages(self) -> list:
        """ Принимает список с объектами класса Page (со ссылками на подстраницы) и отдаёт массив с подстраницами
        """
        sub_pages = []
        for page in Parser.get_dict(self.__pages):
            for all_tags in page['all_tags_from_page']:
                for tag_by_selector in all_tags['tags']:
                    for atrib_key, atrib_value in tag_by_selector['atribs'].items():
                        # if atrib_key == 'src':
                        if atrib_key == 'href':
                            sub_pages.append(atrib_value)

        return sub_pages

    def parse_subpages(self):
        """ Парсинг подстраниц 
        """
        self.__pages = []
        # self.__subpage_selectors = [value for key, value in self.__subpage_selectors.items()]
        self.subpage_urls = [
            urljoin(self.__site_url, url) for url in self.subpage_urls]  # Складываем адреса, чтобы полуить полные

        # for url in self.subpage_urls:
        url = self.subpage_urls[0]
        self.__get_request(url)
        try:
            if self.__req.status_code == 200:
                soup = BeautifulSoup(self.__req.text, 'html.parser')
                p = Page(
                    url=url,
                    soup=soup,
                    selectors=self.__subpage_selectors,
                    subpage_selectors=True
                )
                self.__pages.append(p)
                print(p.get_dict())
            else:
                self.__error = str(f'Exception: {self.__req}')
        except Exception as ex:
            print(ex)
        return self.get_JSON(sort_keys=True, indent=4)

    def parser(self):
        """ Когда точно нет коллизии
        """
        self.parse()    # взять все url пути на посты
        ret_json = self.parse_subpages()    # запарсить посты
        return ret_json

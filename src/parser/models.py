import xml.etree.ElementTree as ET
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import eel
import requests
from django.db import models
import json


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
                 '_Page__elements', '_Page__selector')

    def __init__(self, url, elements, selector=None):
        self.__error = ''
        self.__url = ''
        self.__elements = tuple([])
        self.__selector = selector
        if isinstance(url, (str)):
            if self.check_site(url):
                self.__url = url
            else:
                self.__error = 'This site does not open'
        else:
            self.__error = 'url is not string'
        # Creating and sorting empty lists
        try:
            self.__elements = list(filter(None, elements))
            # print(self.__elements)
            self.__elements = tuple([{
                'selector': self.__selector,
                'html_tags': [j for j in i]
            } for i in self.__elements])
        except:
            self.__error = 'Incorrect data type (elements!=[[HtmlItem,...],...])'

    def print_error(self):
        print(self.__error)
        return self.__error

    def get_dict(self):
        # print([[j.get_dict() for j in i] for i in self.__elements])
        return {
            'url': self.__url,
            'elements': self.__elements,
            'error': self.__error
        }

    def check_site(self, site_name):
        try:
            requests.get(site_name)
            return True
        except:
            self.__error = 'Unknown site'
            return False


class Parser:
    """ Парсер
        Запуск:
        1) Создать класс
        2) Применить метод parse()
        3) Желательно работать с JSON форматом, т.к так проще (метод get_JSON())
    """
    STOP = False    # функция остановки парсера (не доделано, нужно её добавить асинхронность)

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def __init__(self, site_url, selectors=None, multipage=None, number_of_readable_pages=1000000):
        self.__error = ''
        if self.check_site(site_url):
            self.__site_url = site_url
        else:
            self.__site_url = None
        self.__selectors = selectors
        self.__multipage = multipage

        self.__req = None
        self.__pages = []
        self.__there_is_the_following_page = True
        self.__counter = number_of_readable_pages
        self.__all_urls = []

        if self.__selectors == [''] or not isinstance(self.__selectors, list) or self.__selectors == []:
            self.__selectors = None
        if self.__selectors != None:
            for el in self.__selectors:
                if not isinstance(el, str):
                    self.__selectors = None
        if self.__multipage == '' or not isinstance(self.__multipage, str):
            self.__multipage = None

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
            while self.__there_is_the_following_page and counter < self.__counter and self.STOP == False:
                try:
                    eel.print_progress(self.__site_url, counter)
                except:
                    pass
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

                if self.__selectors == None:
                    self.__error = str('Exception: Slectors are not selected')
                    self.__pages.append(Page(url=self.__site_url, elements=[[
                        self.__create_HtmlItem(item=item) for item in soup.find_all()]  # foreach in soup items
                    ]))
                else:
                    self.__pages.append(
                        Page(url=self.__site_url,
                             elements=[
                                 [self.__create_HtmlItem(item=item) for item in soup.select(
                                     selector)]    # foreach in soup items
                                 for selector in self.__selectors]  # foreach in selectors
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

        if self.STOP:
            self.__error += '\tThe stop button was pressed'
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

    def __create_HtmlItem(self, item):
        root = ET.fromstring(str(item))

        return {
            'tag': root.tag,
            'atribs': root.attrib
        }

    def __get_request(self, url, params=None):
        req = requests.get(
            url, headers=self.HEADERS, params=params)
        self.__req = req
        self.site_url = url
        return self.__req
        # print(self.__req)

    @staticmethod
    def get_JSON(pages, sort_keys=False, indent=None) -> json:
        """ Принимает список из классов Page
        """
        if not isinstance(pages, (tuple, list)) or not [isinstance(page, Page) for page in pages]:
            raise TypeError
        return json.dumps([el.get_dict() for el in pages], sort_keys=sort_keys, indent=indent)

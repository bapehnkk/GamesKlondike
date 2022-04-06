from re import L
from django.http import HttpResponse
from .models import Parser
from src.posts.models import PostGame
# parser_test()


def start_parser(request):
    print(f'\r\n{0}\r\n')
    url = 'https://store.epicgames.com/ru/browse?sortBy=releaseDate&sortDir=DESC&count=40'
    selector_link_to_subpage = [
        'section > section > ul > li> div > div > div > a']
    multipage = '#dieselReactWrapper > div > div > main > div > div > div > div > div > section > div > div > div > section > div > section > nav > ul > li:last-child > a'

    subpage_selectors = {
        'Title_selector': 'div > div > main > div > div > div > div > div > div > div > div > h1 > div > span',
        'Description_selector': 'div > div > main > div > div > div > div > div > div > div > div > div > div > div > div > span',
        'Reliase_date_selector': 'div > div > main > div > div > div > div > div > div > div > aside > div > div > div > div > div > div > div > span > time',
        'Tags_selector':'div > div > main > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div > div > ul > li',
        'img_selector': 'div > div > main > div > div > div > div > div > div > div > aside > div > div > div > div > div > div > div > div > div > img',
    }

    p = Parser(url,
               selector_link_to_subpage=selector_link_to_subpage,
               multipage=None,
               subpage_selectors=subpage_selectors)
    ret = p.parser()
    return HttpResponse(ret, content_type="application/json")

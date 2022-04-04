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
        'title_selector': 'div > div > main > div > div > div > div > div > div > div > div > h1 > div > span',
        'text_selector': 'div > div > div > div > div > div> div > div > div > div > div > div > div > span',
        'img_selector': 'div > div > main > div > div > div > div > div > div > div > div > div > div > div > div > ul > li > div > div > div > div > img'
    }

    p = Parser(url,
               selector_link_to_subpage=selector_link_to_subpage,
               multipage=None,
               subpage_selectors=subpage_selectors)
    ret = p.parser()
    return HttpResponse(ret, content_type="application/json")

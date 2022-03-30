from re import L
from django.http import HttpResponse
from .models import Parser
from src.posts.models import PostGame 
# parser_test()


def start_parser(request):
    print(f'\r\n{0}\r\n')
    url = 'https://store.epicgames.com/ru/browse?sortBy=releaseDate&sortDir=DESC&count=40'
    selectors = [
        'section > section > ul > li> div > div > div > a > div > div > div > div > div > img',
        'section > section > ul > li > div > div > div > a > div > div > div > span > div']
    multipage = '#dieselReactWrapper > div > div > main > div > div > div > div > div > section > div > div > div > section > div > section > nav > ul > li:last-child > a'
    p = Parser(url, selectors=selectors, multipage=multipage)
    pages = p.parse()
    ret = p.get_JSON(pages, sort_keys=True, indent=4)
    return HttpResponse(ret, content_type="application/json")

def write_to_DB(pages: list):
    
    for page in pages:
        # page['url']
        # page['error']
        # page['all_tags_from_page']
        for elments in page['all_tags_from_page']:
            pass
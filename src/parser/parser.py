from django.http import HttpResponse
from .models import Parser

# parser_test()


def start_parser(request):
    print(f'\r\n{0}\r\n')
    url = 'https://store.epicgames.com/ru/browse?sortBy=releaseDate&sortDir=DESC&count=40'
    selectors = [
        'section > section > ul > li> div > div > div > a > div > div > div > div > div > img']
    multipage = '#dieselReactWrapper > div > div.css-xxkdgb > main > div:nth-child(2) > div > div > div > div > section > div > div.css-yh460 > div > section > div > section > nav > ul > li:nth-child(8) > a'
    p = Parser(url, selectors=selectors, multipage=multipage)
    pages = p.parse()
    ret = p.get_JSON(pages, sort_keys=True, indent=4)
    print(type(pages[0]))
    return HttpResponse(ret, content_type="application/json")

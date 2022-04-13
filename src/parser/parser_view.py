from django.shortcuts import redirect, render
from django.http import JsonResponse


from .models import ParseUrl, Parser
from src.posts.models import PostGame as PG
from django.views.generic.base import View
from .forms import ParseUrlForm

# is_superuser decorators
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test


class ParserView(View):
    """ Работа с парсером через интерфейс
    """

    template = 'parser/parser_view.html'

    # is_superuser
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request):
        data = {
            'ParseUrl': ParseUrl.objects.all(),
        }
        return render(request, self.template, data)


class ParserJSON(View):
    # is_superuser
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request, pk):
        data = {
            'Json': ParseUrl.objects.get(id=pk).JSON,
        }
        return JsonResponse(data['Json'], safe=False)


class ParserStart(View):
    # is_superuser
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def get(self, request, pk):
        obj = ParseUrl.objects.get(id=pk)
        obj.JSON = self.start_parser()
        obj.save()
        data = {
            'Json': obj.JSON,
        }
        return redirect('/parser/')

    # @method_decorator(user_passes_test(lambda u: u.is_superuser))   # is_superuser
    # def post(self, request):
    #     form = ParseUrlForm(request.POST)
    #     if form.is_valid():
    #         print(f'\r\nVALID\r\n')
    #         form.save()
    #         data = {
    #             'parser_json': ParseUrl.objects.all(),
    #         }
    #         return render(request, self.template, data)
    #     else:
    #         data = {
    #             'errors': form.errors,
    #             'ParseUrl': ParseUrl.objects.all(),
    #             }
    #         return render(request, self.template, data)

    @staticmethod
    def start_parser(
        url='https://store.epicgames.com/en/browse?sortBy=releaseDate&sortDir=DESC&count=40',
        selector_link_to_subpage=[
            'section > section > ul > li> div > div > div > a'],
        multipage='#dieselReactWrapper > div > div > main > div > div > div > div > div > section > div > div > div > section > div > section > nav > ul > li:last-child > a',

        subpage_selectors={
            'Title_selector': 'div > div > main > div > div > div > div > div > div > div > div > h1 > div > span',
            'Description_selector': 'div > div > main > div > div > div > div > div > div > div > div > div > div > div > div > span',
            'Reliase_date_selector': 'div > div > main > div > div > div > div > div > div > div > aside > div > div > div > div > div > div > div > span > time',
            'Tags_selector': 'div > div > main > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div > div:nth-child(1) > div > div > ul > li',
            'img_selector': 'div > div > main > div > div > div > div > div > div > div > aside > div > div > div > div > div > div > div > div > div > img',
        }
    ):
        print(f'\r\n{0}\r\n')
        p = Parser(url,
                   selector_link_to_subpage=selector_link_to_subpage,
                   multipage=None,
                   subpage_selectors=subpage_selectors)
        return p.parser()

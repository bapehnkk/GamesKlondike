from django.contrib import admin


from .models import ParseUrl, PageSelector, SubpageSelector

admin.site.register(ParseUrl)
admin.site.register(PageSelector)
admin.site.register(SubpageSelector)
from django.forms import ModelForm 

from .models import ParseUrl 

class ParseUrlForm(ModelForm):
    class Meta: 
        model = ParseUrl
        fields = ('SiteName', 'SiteURL', 'SubPageURL', 'NextPageUrl')
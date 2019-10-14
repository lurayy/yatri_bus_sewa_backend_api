''' Views module of api '''
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Layout
from .utils import model_to_dict


@require_http_methods(['GET'])
def layouts(request):
    ''' View for handling tasks related to layout model '''
    return JsonResponse({'layouts': model_to_dict(Layout)})

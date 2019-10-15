''' Views module of api '''
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Layout
from .utils import layout_to_json, json_to_layout


@require_http_methods(['GET', 'POST'])
def layouts(request):
    ''' View for handling tasks related to layout model '''
    if request.method == "POST":
        try:
            request_json = json.loads(request.body.decode('utf-8'))
            json_to_layout(request_json)
            return JsonResponse({'success': 'Successfully created the layout'})
        except (KeyError, json.decoder.JSONDecodeError) as exp:
            return JsonResponse({'error': f'{exp.__class__.__name__}: {exp}'})
    output = []
    layout_objects = Layout.objects.all()
    for layout in layout_objects:
        output.append(layout_to_json(layout))
    return JsonResponse({'layouts': output})

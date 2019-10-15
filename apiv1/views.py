''' Views module of api '''
import json

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import Layout, Route
from .serializers import RouteSerializer
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
    response = []
    layout_objects = Layout.objects.all()
    for layout in layout_objects:
        response.append(layout_to_json(layout))
    return JsonResponse({'layouts': response})


@require_http_methods(['GET'])
def routes(request):
    ''' View for handling tasks related to route model '''
    response = []
    route_objects = Route.objects.all()
    for route in route_objects:
        response.append(RouteSerializer(route))
    return JsonResponse({'routes': response})

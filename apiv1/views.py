
''' Views module of api '''
import json 

from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from .models import Layout, Seat
from .utils import model_to_dict


@require_http_methods(['GET', 'POST'])
def layouts(request):
    ''' View for handling tasks related to layout model '''
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            json_obj = json.loads(json_str)
            layout_data = json_obj['data'] 
            layout_name = json_obj['name']
            layout = Layout.objects.create(name = str(layout_name))
            layout.save()
            print("layout saved")
            for x in range(len(layout_data)):
                for y in range(len(layout_data[x])):
                    if str(layout_data[x][y]['state']) == "available":
                        s = Seat.objects.create(layout = layout, seat_number = str(x)+","+str(y), state = str(layout_data[x][y]['state']))
                        s.save()
            return HttpResponse(status=201)
        except:
            return HttpResponseBadRequest
    else:
        return JsonResponse({'layouts': model_to_dict(Layout)})
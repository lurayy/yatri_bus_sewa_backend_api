from django.shortcuts import render, HttpResponseRedirect, HttpResponse
import json
from .models import Layout 


def save_layout(request):
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            json_obj = json.loads(json_str)
            layout_data = json.dumps(json_obj['data']) 
            layout_name = json_obj['name']
            layout = Layout.objects.create(name = str(layout_name), layout = str(layout_data), width = int(len(json_obj['data'][0])), height = int(len(json_obj['data'])))
            layout.save()
            return HttpResponse("Good")
        except:
            return HttpResponse("Error saving layout")          
    else:
        return HttpResponse('Bad Request')
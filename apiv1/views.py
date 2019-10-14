from django.shortcuts import render, HttpResponse
from .models import Layout

def save_layout(request):
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            json_obj = json.loads(json_str)
            layout_data = json.dumps(json_obj['data']) 
            layout_name = json_obj['name']
            layout = Layout.objects.create(name = str(layout_name), grid = str(layout_data))
            layout.save()
            return HttpResponse("Good")
        except:
            return HttpResponse("Error saving layout")          
    else:
        return HttpResponse('Bad Request')


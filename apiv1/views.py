from django.shortcuts import render, HttpResponse
from .models import Layout, Seat
import json


def save_layout(request):
    if request.method == "POST":
        try:
            json_str = request.body.decode(encoding='UTF-8')
            json_obj = json.loads(json_str)
            layout_data = json_obj['data'] 
            layout_name = json_obj['name']
            layout = Layout.objects.create(name = str(layout_name), seat_count = 0)
            layout.save()
            seat_count = 0
            print("layout saved")
            for x in range(len(layout_data)):
                for y in range(len(layout_data[x])):
                    if str(layout_data[x][y]['state']) == "available":
                        s = Seat.objects.create(layout = layout, seat_number = str(x)+","+str(y), state = str(layout_data[x][y]['state']))
                        s.save()
                        seat_count = seat_count + 1 
            layout.seat_count = seat_count
            layout.save()
            return HttpResponse("Good")
        except:
            return HttpResponse("Error saving layout")          
    else:
        return HttpResponse('Bad Request')


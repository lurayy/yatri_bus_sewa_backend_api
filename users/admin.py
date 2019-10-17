''' Admin module of api '''
from django.contrib import admin
from .models import Operator, Agent, Customer

admin.site.register(Operator)
admin.site.register(Agent)
admin.site.register(Customer)

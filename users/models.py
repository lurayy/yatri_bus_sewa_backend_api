# from django.db import models
# from django.contrib.auth.models import AbstractUser
# # Create your models here.

# class CustomUserBase(AbstractUser):
#     is_operator = models.BooleanField(default= False)
#     is_agent = models.BooleanField(default= False)
#     is_customer = models.BooleanField(default= True)

# class Operator(models.Model):
#     REQUIRED_FIELDS = ('user',)
#     user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True, related_name = 'operator', unique = True)

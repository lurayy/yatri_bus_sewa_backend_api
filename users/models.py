import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserBase(AbstractUser):
    '''
    Model that extends the AbstractUser model of Django to create a common
    CustomUserBase which can be used to create different user classes
    '''
    USER_TYPES = (
        ('OPERATOR', "Operator"),
        ('CUSTOMER', "Customer"),
        ('AGENT', "Agent")
    )
    user_type = models.CharField(max_length=9, choices=USER_TYPES, default="Customer")
    unique_id = models.UUIDField(default=uuid.uuid4, unique=True)

class Operator(models.Model):
    ''' Model class for the Operator user base '''
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUserBase, on_delete=models.CASCADE,
                                primary_key=True, related_name='operator', unique=True)

class Customer(models.Model):
    ''' Model class for the Customer user base '''
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUserBase, on_delete=models.CASCADE,
                                primary_key=True, related_name='customer', unique=True)

class Company(models.Model):
    '''
    Model used to save a company profile, using which we can later
    calculate total revenue thorugh that paticular company or credit that they own.
    '''
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class Agent(models.Model):
    ''' Model class for the Agent user base '''
    REQUIRED_FIELDS = ('user',)
    user = models.OneToOneField(CustomUserBase, on_delete=models.CASCADE,
                                primary_key=True, related_name='agent', unique=True)
    company_name = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    credit = models.IntegerField(default=0)

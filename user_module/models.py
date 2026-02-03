from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

def phone_number_validator(number:str):
    if not number.isnumeric():

        raise ValidationError('phone number cannot have non numberic characters')


# Create your models here.
class User(AbstractUser):
    phone_number=models.CharField(max_length=11,validators=[phone_number_validator],verbose_name='user phone number (numberic)',null=False,blank=False)
    activation_code=models.CharField(max_length=64,verbose_name="this code will be sent to users emails then users will use this code to activate their accounts"
                                     ,null=False,blank=False)
    balance=models.DecimalField(max_digits=5,decimal_places=3,default=00.00)





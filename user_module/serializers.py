from .models import User
from rest_framework import serializers

class User_Update_Serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['phone_number','first_name','last_name']

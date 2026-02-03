import re

from django.core.exceptions import ValidationError
from rest_framework import serializers
from user_module.models import User

password_pattern=r'(?=.*[0-9].*)(?=.*[A-Z].*)'
class Login_Serializer(serializers.Serializer):
    email_username=serializers.CharField(max_length=100,label='email_username',required=True)
    password=serializers.CharField(max_length=100,label='password',required=True)


class Signup_Serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','phone_number']
    def validate(self, attrs):
        password=self.data.get('password')
        if re.match(password_pattern,password):
            raise ValidationError('the password must contain at least one uppercase character and one numeric character')
        return super().validate(attrs)


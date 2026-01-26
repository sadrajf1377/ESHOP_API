from rest_framework import serializers

class Login_Serializer(serializers.Serializer):
    email_username=serializers.CharField(max_length=100,label='email_username',required=True)
    password=serializers.CharField(max_length=100,label='password',required=True)
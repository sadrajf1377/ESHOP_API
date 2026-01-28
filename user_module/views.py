from django.shortcuts import render
from rest_framework.generics import UpdateAPIView

from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import User_Update_Serializer
class Update_User_Info(UpdateAPIView):
    serializer_class = User_Update_Serializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    http_method_names = ['PUT']
    def options(self, request, *args, **kwargs):
        options=super().options(*args,**kwargs)
        fields='-'.join([str(x) for x in User_Update_Serializer.fields])
        options['guide']=f'send your string json data and add the following fields :{fields}'
        return options

# Create your views here.

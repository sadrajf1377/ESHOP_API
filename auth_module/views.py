from django.db.models import Q
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from user_module.models import User
from rest_framework.permissions import AllowAny
from .serializers import Login_Serializer
class Login(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data=request.data
        ser=Login_Serializer(data)
        if ser.is_valid():
            try:
                username_or_email=ser.data.get('email_username')
                password=ser.data.get('password')
                user=User.objects.filter(Q(username=username_or_email)|Q(email=username_or_email))
                if user.check_password(password):
                    refresh=RefreshToken(request)
                    access=refresh.access_token
                    return Response(data={'message':'login successfull','access_token':str(access.token),'refresh_token':str(refresh.token)},status=200)
                else:
                    return Response(data={'message':'user not found!'},status=404)
            except User.DoesNotExist:
                    return Response(data={'message': 'user not found!'}, status=404)
            except:
                return Response(data={'message':'an error has happend!please try again'},status=500)
        else:
            return Response(data={'message':'invalid data format,please chekc the option for the correct format '},status=400)
    def options(self, request, *args, **kwargs):
        options=super().options(*args,**kwargs)
        options['data_format']="type=json string,format={'email_username':'your email or username','password':'your password'}"
        return options




# Create your views here.

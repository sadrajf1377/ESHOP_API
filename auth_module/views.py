from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken,RefreshToken
from user_module.models import User
from rest_framework.permissions import AllowAny
from .serializers import Login_Serializer,Signup_Serializer
from utils.email_services import send_mails
from rest_framework.throttling import AnonRateThrottle
class Login(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['OPTIONS','POST']
    throttle_classes = [AnonRateThrottle]
    def post(self,request):
        data=request.data
        ser=Login_Serializer(data=data)
        if ser.is_valid():
            try:
                username_or_email=ser.data.get('email_username')
                password=ser.data.get('password')
                user=User.objects.filter(Q(username=username_or_email)|Q(email=username_or_email),is_active=True)
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


class Signup(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['OPTIONS', 'POST']
    throttle_classes = [AnonRateThrottle]
    def post(self,request):
        ser=Signup_Serializer(data=request.data)
        if ser.is_valid():
            try:
                with transaction.atomic():
                    data:dict=ser.data

                    password=data.get('password')
                    data['password']=make_password(password)
                    activation_code=get_random_string(length=64)
                    data['activation_code']=activation_code
                    us=User(**data)
                    us.save()
                    send_mails.delay('account_activation','Activation_Email.html',data.get('email'),{'activation_code':activation_code,'user_id':us.id})
                    return Response(data={'message':'signed up successfully!to activate your account,please click on the link we sent to your email'},status=201)
            except KeyError as ke:
                return Response(data={'message':'incorrect data,please check the errors','errors':str(ke)},status=400)
        else:
            return Response(data={'message': 'incorrect data,please check the errors', 'errors': str(ser.errors)}, status=400)




# Create your views here.
class Activate_Account(View):
    @csrf_exempt
    def post(self,request):

        try:
            user_id = request.POST.get('user_id')
            act_code=request.POST.get('act_code')
            user=User.objects.get(id=user_id)
            if not user.activation_code == act_code:
                return Response(data={'message':'user not found or the link was expired!'},status=404)
            else:
                user.is_active=True
                user.save()
                return Response(data={'message':'your account was updated successfully'},status=201)
        except Exception as e:
            if isinstance(e,User.DoesNotExist):
                return Response(data={'message': 'user not found'}, status=404)
            elif isinstance(KeyError):
                return Response(data={'message':'the input data was invalid!'},status=400)
            else:
                return Response(data={'message':'an error happend!please try again'},status=500)



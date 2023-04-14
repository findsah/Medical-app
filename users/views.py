import math
import random
from smtplib import SMTPException
from django.core.mail import send_mail, EmailMessage

from users.models import MedicalHistory, SuperUser, UserOtp
from .serializers import LoginUserSerializer, MedicalHistorySerializer, OTPSerializer, RegistrationSerializer, UserSerializer
from rest_framework import status, generics, viewsets, permissions
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token as AuthToken
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView
# Create your views here.

def send_otp_on_mail(username, email, save_otp=True) :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    # try:
    #     htmlgen = '<p>Welcome {} Your OTP is <strong>{}</strong>, Use this otp to verify your mail </p>'.format(username, OTP)
    #     send_mail('OTP request', OTP ,'<your gmail id>',[email], fail_silently=False, html_message=htmlgen)
    # except SMTPException as e:          # It will catch other errors related to SMTP.
    #     print('There was an error sending an email.', e)
    # except:                             # It will catch All other possible errors.
    #     print("Mail Sending Failed!") 
    if save_otp:
        save_otp = UserOtp(otp_number=OTP, user_email=email)
        save_otp.save()
    return OTP

class EmailVerifyAPI(generics.GenericAPIView): 
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = OTPSerializer(data=request.data) 
        if serializer.is_valid(): 
            user_email = request.POST.get('email')
            otp = request.POST.get('otp')
            if user_email and otp:
                try: 
                    obj = UserOtp.objects.get(user_email=user_email, otp_number=otp)
                except UserOtp.DoesNotExist:
                    obj=None 
                if obj is not None:
                    user=SuperUser.objects.get(email=obj.user_email)
                    user.is_active = True
                    user.save() 
                    obj.delete()
                    return Response({'msg':'Email verify sucessfully', 'status':status.HTTP_200_OK})
                else:
                    return Response({'details':'Invalid OTP or Email'})
            return Response({'errors':'user email and opt is required'})
        return Response(serializer.errors)


class ResendOTPAPI(generics.GenericAPIView):  
    permission_classes = [permissions.AllowAny]
    def post(self, request, *args, **kwargs): 
        user_email = request.data.get('email') 
        if user_email =='' or user_email is None or len(user_email) < 5: 
            return Response({'details':'A Valid email is required.'})
        try: 
            obj = UserOtp.objects.get(user_email=user_email)
        except UserOtp.DoesNotExist:
            obj=None 
        if obj:
            obj.otp_number = send_otp_on_mail('Guest', user_email, save_otp=False) 
            obj.save() 
            return Response({'msg':'OTP has been send on {}'.format(user_email), 'status':status.HTTP_200_OK})
        else:
            return Response({'details':'OPPS! your email not found. Please register.'}) 

class RegisterAPI(generics.GenericAPIView): 
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save() 
            otp = send_otp_on_mail(user.first_name, user.email)
            token, created = AuthToken.objects.get_or_create(user=user)
            return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key,
            "otp":otp
            })
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginUserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = AuthToken.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

class LoggedInUser(generics.RetrieveAPIView):
  # permission_classes = [
  #     permissions.IsAuthenticated
  # ]
  serializer_class = UserSerializer
  def get_object(self):
    return self.request.user
  
class MedicalHistoryAPI(generics.GenericAPIView):
    # permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, format=None):
        request.data['user'] = request.user.id
        serializer = MedicalHistorySerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                inst = MedicalHistory.objects.get(user=request.user)
            except MedicalHistory.DoesNotExist:
                inst = None
            if inst:
                inst.attachment = request.FILES['attachment']
                inst.save()
                return Response({
                    'data':MedicalHistorySerializer(inst).data,
                    'status':status.HTTP_200_OK
                })
            c = MedicalHistory(user=request.user, attachment = request.FILES['attachment'])
            c.save()
            return Response({
                'data':MedicalHistorySerializer(c).data,
                'status':status.HTTP_201_CREATED
            })
        return Response({
                'data':serializer.errors,
                'status':status.HTTP_400_BAD_REQUEST
            })

    def get(self, request, pk=None):
        user_id = self.request.user 
        if pk:
            try:
                inst = MedicalHistory.objects.get(id=pk, user=user_id)
            except MedicalHistory.DoesNotExist:
                inst = None
        
            return Response({
                'data':MedicalHistorySerializer(inst).data,
                'status':status.HTTP_200_OK
            })
        dataSet = MedicalHistory.objects.filter(user=user_id)
        return Response({
            'data':MedicalHistorySerializer(dataSet, many=True).data,
            'status':status.HTTP_200_OK
        })

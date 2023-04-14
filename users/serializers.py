from django.forms import ValidationError
from rest_framework import serializers
from .models import *
from .models import SuperUser as User
from django.contrib.auth import authenticate 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperUser
        fields=["id","email","first_name","last_name","phone","user_type","address"]

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOtp
        fields = ['user_email','otp_number']
    
    def validate_user_email(self, value):
        if value =='' or value is None:
            raise ValidationError('User email is required')

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['id','user', 'attachment']
    
    def validate_attachment(self, value):
        if not value:
            raise ValidationError('Attachment is required.')



class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200) 
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    phone = serializers.IntegerField()
    address = serializers.CharField(max_length=300) 
    user_type = serializers.CharField()
    password = serializers.CharField(style={'input_type':  'password'}, write_only = True)
    confirm_password = serializers.CharField(style={'input_type':  'password'}, write_only = True)


    # class Meta:
    # 	model = SuperUser
    # 	fields = ['email', 'name', 'first_name', 'last_name', 'phone', 'country', 'state', 'city', 'zip_code', 'password', 'confirm_password']


    def validate_first_name(self, value): 
        if value=='' or value is None:
            raise serializers.ValidationError("there must be first in your first_name")
        return value 

    def validate_email(self, value):
        """
        Check that the valid email with @gmail.com is provided by the user or not in the given email.
        """
        data = self.get_initial()
        email = data.get('email')
        # password = value
        user_email = SuperUser.objects.filter(email=email)

        if user_email:
            raise ValidationError("User with this email already exists.") 
        return value   


    def save(self):
        account = User( 
            email      = self.validated_data['email'], 
            first_name = self.validated_data['first_name'],
            last_name  = self.validated_data['last_name'],
            phone      = self.validated_data['phone'],
            address    = self.validated_data['address'],  
            user_type  = self.validated_data['user_type'],  
            is_active  = False,  
            )

        password = self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']

        if password != confirm_password:
            raise ValidationError(_("Both passwords doesn't match"))
        account.set_password(password)
        account.save()
        return account 

class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorrect Credentials Passed.')
    
 
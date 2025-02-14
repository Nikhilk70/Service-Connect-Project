from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile, EmployeeRegistration, ServiceRegistry, ServiceRequest, services, Subservices, BookingList
from django.core.mail import send_mail

class RegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = User.objects.create_user(**validated_data)
        profile = UserProfile.objects.create(user=user, phone_number=phone_number)
        profile.generate_otp()

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {profile.otp}',
            'your-email@gmail.com',
            [user.email],
            fail_silently=False,
        )
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'email']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid email or password')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid email or password')

        if not user.profile.is_verified:
            raise serializers.ValidationError('Please verify your OTP before logging in')

        data['user'] = user
        return data

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            profile = user.profile
            print(f"Stored OTP: {profile.otp}")
            print(f"Received OTP: {data['otp']}")
            if profile.otp == data['otp']:
                profile.is_verified = True
                profile.otp = None
                profile.save()
                return {"user": user}
            else:
                raise serializers.ValidationError('Invalid OTP')
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['address', 'state', 'date_of_birth']

class EmployeeRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeRegistration
        fields = ['name','age','phonne_number','role']
        
    def create(self, validated_data):
        return EmployeeRegistration.objects.create(**validated_data)
    
class ServiceRegistrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRegistry
        fields = ['employee','service','min_price','max_price','description']
        
class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = ['service_registry','title','description','from_time','to_time']
        
        def create(self, validated_data):
            return ServiceRequest.objects.create(**validated_data)
        
class BookingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingList
        fields = ['id', 'customer','employee','booking_date']
from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import generics, status,permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, OTPVerificationSerializer, UserDetailsSerializer, UserSerializer, EmployeeRegisterSerializer,ServiceRegistrySerializer,ServiceRequestSerializer,BookingListSerializer
from .models import UserProfile, EmployeeRegistration,ServiceRegistry,BookingList,ServiceRequest
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication




class UserListAV(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserlDetailsView(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = UserSerializer(user)
            return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=204)
    
    
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username
            }
        }, status=status.HTTP_200_OK)

class OTPVerificationView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "message": "OTP verified successfully. Account activated.",
            "token": token.key
        }, status=status.HTTP_200_OK)

class UserDetailsView(generics.CreateAPIView):
    serializer_class = UserDetailsSerializer
    queryset = UserProfile.objects.all()
    def get_serializer_context(self):
        return {'request': self.request}
    
class EmployeeRegisterView(generics.CreateAPIView):
    serializer_class = EmployeeRegisterSerializer
    
class EmployeeListView(generics.ListAPIView):
    queryset = EmployeeRegistration.objects.all()
    serializer_class = EmployeeRegisterSerializer

class ServiceListView(generics.ListAPIView):
    queryset = ServiceRegistry.objects.all()
    serializer_class = ServiceRegistrySerializer
    
class ServiceDetailsView(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            try:
                Service = ServiceRegistry.objects.get(pk=pk)
            except ServiceRequest.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = ServiceRegistrySerializer(Service)
            return Response(serializer.data)
    
class ServiceRequestView(generics.CreateAPIView):
    serializer_class = ServiceRequestSerializer
    
class ServiceRequestList(generics.ListAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    
class BookingListView(generics.ListAPIView):
    queryset = BookingList.objects.all()
    serializer_class = BookingListSerializer
    
class RequestDetailsView(APIView):
    def get(self, request, pk):
        if request.method == 'GET':
            try:
                user = ServiceRequest.objects.get(pk=pk)
            except ServiceRequest.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
            serializer = ServiceRequestSerializer(user)
            return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            user = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        serializer = ServiceRequestSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        try:
            user = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=204)
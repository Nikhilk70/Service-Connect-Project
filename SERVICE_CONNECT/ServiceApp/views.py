from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import generics, status,permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, OTPVerificationSerializer, UserDetailsSerializer, UserSerializer, EmployeeRegisterSerializer,ServiceRegistrySerializer,ServiceRequestSerializer,BookingListSerializer, RatingSerializer, ComplaintSerializer
from .models import UserProfile, EmployeeRegistration,ServiceRegistry,BookingList,ServiceRequest,RatingModel, Complaint
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



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
    
class CustomerPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page'
    
class ServiceRequestView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceRequestSerializer
    
class ServiceRequestList(generics.ListAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    pagination_class = CustomerPagination
    
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
    
class RatingViewSet(viewsets.ModelViewSet):
    queryset = RatingModel.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = RatingModel.objects.all()
        service_id = self.request.query_params.get('service', None)
        employee_id = self.request.query_params.get('employee', None)

        if service_id:
            queryset = queryset.filter(select_service_id=service_id)
        if employee_id:
            queryset = queryset.filter(select_employee_id=employee_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['GET'])
    def my_ratings(self, request):
        ratings = RatingModel.objects.filter(user=request.user)
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def service_ratings(self, request):
        service_id = request.query_params.get('service_id')
        if not service_id:
            return Response(
                {"error": "service_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ratings = RatingModel.objects.filter(select_service_id=service_id)
        serializer = self.get_serializer(ratings, many=True)

        avg_rating = ratings.values_list('rating', flat=True)
        rating_map = {
            'VERY_BAD': 1,
            'BAD': 2,
            'GOOD': 3,
            'VERY_GOOD': 4,
            'EXCELLENT': 5
        }
        
        if ratings:
            numeric_ratings = [rating_map[r] for r in avg_rating]
            average = sum(numeric_ratings) / len(numeric_ratings)
        else:
            average = 0

        return Response({
            'ratings': serializer.data,
            'average_rating': average,
            'total_ratings': len(ratings)
        })
        

class ComplaintListCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ComplaintSerializer
        
# class ServiceRequestView(generics.CreateAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     serializer_class = ServiceRequestSerializer
        
class ComplaintDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Complaint.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]
    
from django.urls import path
from .views import RegisterView, LoginView, OTPVerificationView, UserDetailsView, UserListAV,EmployeeRegisterView, EmployeeListView, ServiceListView,ServiceRequestView
from .views import BookingListView,UserlDetailsView,ServiceRequestList,RequestDetailsView,ServiceDetailsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('list/', UserListAV.as_view(), name='list'),
    path('list/<int:pk>/', UserlDetailsView.as_view(), name='listdetails'),
    path('bookinglist/', BookingListView.as_view(), name='bookinglist'),
    path('register/', RegisterView.as_view(), name='register'),
    path('EmployeRegstr/', EmployeeRegisterView.as_view(), name='EmployeRegstr'),
    path('Emplylist/', EmployeeListView.as_view(), name='Employelist'),
    path('Servicelist/', ServiceListView.as_view(), name='Servicelist'),
    path('Servicelist/<int:pk>/', ServiceDetailsView.as_view(), name='ServiceListDetails'),
    path('ServiceRequest/', ServiceRequestView.as_view(), name='ServiceRequest'),
    path('ServiceRequestList/', ServiceRequestList.as_view(), name='ServiceRequestList'),
    path('ServiceRequestList/<int:pk>/', RequestDetailsView.as_view(), name='ServiceRquestDetails'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp/', OTPVerificationView.as_view(), name='verify-otp'),
    path('user-details/', UserDetailsView.as_view(), name='user-details'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.contrib import admin
from .models import UserProfile, EmployeeRegistration, ServiceRegistry, ServiceRequest, services, Subservices, BookingList

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EmployeeRegistration)
admin.site.register(ServiceRegistry)
admin.site.register(ServiceRequest)
admin.site.register(services)
admin.site.register(Subservices)
admin.site.register(BookingList)
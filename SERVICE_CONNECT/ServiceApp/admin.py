from django.contrib import admin
from .models import UserProfile, EmployeeRegistration, ServiceRegistry, ServiceRequest, Services, Subservices, BookingList, RatingModel

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(EmployeeRegistration)
admin.site.register(ServiceRegistry)
admin.site.register(ServiceRequest)
admin.site.register(Services)
admin.site.register(Subservices)
admin.site.register(BookingList)
admin.site.register(RatingModel)
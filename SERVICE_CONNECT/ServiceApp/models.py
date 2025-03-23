import random
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    address = models.TextField(blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return str(self.user)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        
        
def validate_file_size(image):
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("The image file size should not exceed 2MB.")

class Services(models.Model):
    title = models.CharField(max_length=50,db_index=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, validators=[validate_file_size]) 
    description = models.TextField()
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])


    def __str__(self):
        return self.title


class Subservices(models.Model):
    title = models.CharField(max_length=50,db_index=True)
    services = models.ForeignKey(Services, on_delete=models.CASCADE, related_name="subservices")
    image = models.ImageField(upload_to='images/', null=True, blank=True, validators=[validate_file_size])
    description = models.TextField()
    
class EmployeeRegistration(models.Model):
    name = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    phonne_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(default="Employee",max_length=256)
    
    def __str__(self):
        return (self.name + ' : ' + self.role)
    
class ServiceRegistry(models.Model):
    employee = models.ForeignKey(EmployeeRegistration,on_delete=models.CASCADE)
    service = models.ForeignKey(Services,on_delete=models.CASCADE)
    min_price = models.PositiveIntegerField()
    max_price = models.PositiveIntegerField()
    description = models.TextField()
    
    def __str__(self):
        return str(self.service)


    
class ServiceRequest(models.Model):
    service_registry = models.ForeignKey(ServiceRegistry, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.title)
    
class BookingList(models.Model):
    customer = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    employee = models.ForeignKey(EmployeeRegistration,on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    
class RatingModel(models.Model):
    RATING_CHOICES = (
        ('VERY_BAD', 'Very Bad'),
        ('BAD', 'Bad'),
        ('GOOD', 'Good'),
        ('VERY_GOOD', 'Very Good'),
        ('EXCELLENT', 'Excellent'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    service = models.ForeignKey('Services', on_delete=models.CASCADE, related_name='service_ratings')
    employee = models.ForeignKey('EmployeeRegistration', on_delete=models.CASCADE, related_name='employee_ratings')
    rating = models.CharField(
        max_length=20,
        choices=RATING_CHOICES,
        default='GOOD'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee} - {self.get_rating_display()}"


class RatingModel(models.Model):
    RATING_CHOICES = (
        ('VERY_BAD', 'Very Bad'),
        ('BAD', 'Bad'),
        ('GOOD', 'Good'),
        ('VERY_GOOD', 'Very Good'),
        ('EXCELLENT', 'Excellent'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    select_service = models.ForeignKey('Services', on_delete=models.CASCADE, related_name='service_ratings',default=1, null=True)
    select_employee = models.ForeignKey('EmployeeRegistration', on_delete=models.CASCADE, related_name='employee_ratings', null=True, blank=True)
    rating = models.CharField(
        max_length=20,
        choices=RATING_CHOICES,
        default='GOOD'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.select_employee} - {self.get_rating_display()}"
    class Meta:
        unique_together = ['user', 'select_employee', 'select_service']
        
class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending','Pending'),
        ('In Progress','In Progress'),
        ('Resolved','Resolved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=256)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject} - {self.status}"
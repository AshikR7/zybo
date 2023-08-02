from django.db import models
from django.contrib.auth.models import User

class superAdminModel(models.Model):
    superadmin = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)

class adminModel(models.Model):
    admin = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)

class departmentModel(models.Model):
    department = models.CharField(max_length=30)

class doctorModel(models.Model):
    name = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='static/doctors')
    qualification = models.CharField(max_length=30)

class appointmentsModel(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()
    place = models.CharField(max_length=30)
    date = models.DateField()
    time = models.TimeField()
    department = models.CharField(max_length=30)
    doctor = models.CharField(max_length=30)
    status = models.CharField(max_length=20,default='pending', choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')])

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


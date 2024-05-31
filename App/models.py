from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomLogin(AbstractUser):
    viewPass = models.CharField(max_length = 100)
    userType = models.CharField(max_length = 100)

class UserRegister(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    phone = models.IntegerField()
    country = models.CharField(max_length = 100)
    login_id = models.ForeignKey(CustomLogin,on_delete = models.CASCADE)

    def __str__(self):
        return self.name
    
class CompanyRegister(models.Model):
    company = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    phone = models.IntegerField()
    country = models.CharField(max_length = 100)
    login_id = models.ForeignKey(CustomLogin,on_delete = models.CASCADE)
    
    def __str__(self):
        return self.company
    
class AddEvents(models.Model):
    company = models.CharField(max_length = 100)
    email = models.EmailField(max_length = 100)
    phone = models.IntegerField()
    event = models.CharField(max_length = 100)
    date = models.DateField()
    country = models.CharField(max_length = 100)
    poster = models.ImageField(null=True)
    price = models.CharField(max_length = 100, null=True)
    company_id = models.ForeignKey(CompanyRegister,on_delete = models.CASCADE, null = True)

    def __str__(self):
        return self.company

class EventBook(models.Model):
    event_id = models.ForeignKey(AddEvents, on_delete = models.CASCADE)
    user_id = models.ForeignKey(UserRegister, on_delete = models.CASCADE)
    book_date = models.DateField(auto_now = True)
    company_id = models.ForeignKey(CompanyRegister,on_delete = models.CASCADE, null = True)
    status = models.CharField(max_length = 100, default = "BOOKED", null = True)
    persons = models.IntegerField(null = True)
    credit = models.IntegerField(null = True)
    total_amount = models.IntegerField(null = True)

    def __str__(self):
        return self.event_id.company

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomLogin)
admin.site.register(UserRegister)
admin.site.register(AddEvents)
admin.site.register(CompanyRegister)
admin.site.register(EventBook)
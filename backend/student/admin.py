from django.contrib import admin
from .models import *
# Register your models here.
admin.site.site_header = "Student Models"

admin.site.register(Batch)
admin.site.register(Role)
admin.site.register(StudentProfile)
admin.site.register(StudentVerification)
from django.contrib import admin
from .models import Department, EmployeeProfile, Request

# Register your models here.

admin.site.register(Department)
admin.site.register(EmployeeProfile)

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'employee', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'employee__username')

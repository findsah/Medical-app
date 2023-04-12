from django.contrib import admin
from .models import SuperUser as User, UserOtp
from django.contrib.auth.forms import UserChangeForm,AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserAdmin(UserAdmin):
    ordering=['email']
    form=UserChangeForm
    list_filter = ('is_superuser','is_active','is_staff','last_login')
    list_display_links=['username','email']


admin.site.register(User, UserAdmin) 
admin.site.register(UserOtp) 
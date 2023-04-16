from django.contrib import admin
from .models import SuperUser as User, UserOtp, MedicalHistory
from django.contrib.auth.forms import UserChangeForm,AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserAdmin(UserAdmin):
    ordering=['email']
    form=UserChangeForm
    list_filter = ('is_superuser','is_active','is_staff','last_login')
    list_display_links=['username','email']
    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
                },
            ),
        )

admin.site.register(User, UserAdmin) 
admin.site.register(UserOtp) 
admin.site.register(MedicalHistory) 
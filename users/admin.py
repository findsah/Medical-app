from django.contrib import admin
from .models import Appointment, Heartbeat, MedicalForm, SuperUser as User, UserOtp, MedicalHistory
from django.contrib.auth.forms import UserChangeForm, AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class UserRegisterAdmin(UserAdmin):
    ordering=['email']
    form = UserChangeForm
    list_filter = ('is_superuser','is_active','is_staff','last_login')
    list_display=['email','username','first_name','last_name','user_type','is_active']
    list_display_links=['username','email']
    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('email','password1', 'password2','first_name','last_name','user_type','phone','address'),
                },
            ),
        )
    UserAdmin.fieldsets += (('Extra Fields', {'fields': ('user_type','phone','address' )}),)

class MedicalFormAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "doctor":
            kwargs["queryset"] = User.objects.filter(user_type=2)
        if db_field.name == "patient":
            kwargs["queryset"] = User.objects.filter(user_type=1)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(User, UserRegisterAdmin) 
admin.site.register(UserOtp) 
admin.site.register(MedicalHistory) 
admin.site.register(Heartbeat) 
admin.site.register(Appointment) 
admin.site.register(MedicalForm, MedicalFormAdmin) 
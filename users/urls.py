from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static
from django.conf import settings 
from rest_framework.routers import DefaultRouter 

from users.views import AllUserAPI, AppointmentAPI, HeartbeatAPI, MedicalFormAPI, MedicalHistoryAPI, RegisterAPI, LoginAPI, LoggedInUser, EmailVerifyAPI, ResendOTPAPI

router=DefaultRouter()

# router.register('question_api', views.QuestionModelViewSet, basename='question') 
 
urlpatterns = [ 
    # path('',include(router.urls)), 
    path('all_users/', AllUserAPI.as_view(), name='all_users'), 
    path('all_users/<int:pk>/', AllUserAPI.as_view(), name='all_users'), 
    path('registration/', RegisterAPI.as_view(), name='register'), 
    path('auth/user/', LoggedInUser.as_view()), 
    path('login/', LoginAPI.as_view(), name='login'), 
    path('email_verify/', EmailVerifyAPI.as_view(), name='email_verify'), 
    path('resend_otp/', ResendOTPAPI.as_view(), name='resend_otp'), 
    path('medicl_hitory/', MedicalHistoryAPI.as_view(), name='medicl_hitory'), 
    path('medicl_hitory/<int:pk>/', MedicalHistoryAPI.as_view(), name='get_medicl_hitory'), 
    path('book_appointment/', AppointmentAPI.as_view(), name='book_appointment'), 
    path('book_appointment/<int:pk>/', AppointmentAPI.as_view(), name='get_appointment'), 
    path('heartbeat/', HeartbeatAPI.as_view(), name='heartbeat'), 
    path('heartbeat/<int:pk>/', HeartbeatAPI.as_view(), name='get_heartbeat'), 
    path('medical_form/', MedicalFormAPI.as_view(), name='medical_form'), 
    path('medical_form/<int:pk>/', MedicalFormAPI.as_view(), name='get_medical_form'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Healthcare Admin Dashboard"
admin.site.site_title = "Healthcare Admin Portal"
admin.site.index_title = "Welcome to the Healthcare Portal"
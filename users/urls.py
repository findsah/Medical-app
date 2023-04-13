from django.contrib import admin
from django.urls import include, path 
from django.conf.urls.static import static
from django.conf import settings 
from rest_framework.routers import DefaultRouter 

from users.views import RegisterAPI, LoginAPI, LoggedInUser, EmailVerifyAPI, ResendOTPAPI

router=DefaultRouter()

# router.register('question_api', views.QuestionModelViewSet, basename='question') 

urlpatterns = [ 
    # path('',include(router.urls)), 
    path('registration/', RegisterAPI.as_view(), name='register'), 
    path('auth/user/', LoggedInUser.as_view()), 
    path('login/', LoginAPI.as_view(), name='login'), 
    path('email_verify/', EmailVerifyAPI.as_view(), name='email_verify'), 
    path('resend_otp/', ResendOTPAPI.as_view(), name='resend_otp'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Healthcare Admin"
admin.site.site_title = "Healthcare Admin Portal"
admin.site.index_title = "Welcome to the Healthcare Portal"
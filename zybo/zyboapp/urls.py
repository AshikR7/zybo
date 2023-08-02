from django.urls import path
from .views import *
urlpatterns=[
    path('index/',index),
    path('superregister/',superRegister),
    path('superlogin/',superLogin),
    path('superprofile/',superProfile),
    path('adminregister/',adminRegister),
    path('adminlogin/',adminLogin),
    path('adminprofile/',adminProfile),
    path('adminlist/',adminList.as_view(),name='adminlist'),
    path('adminupdate/<pk>',adminUpdate.as_view(),name='adminupdate'),
    path('admindelete/<pk>',AdminDelete.as_view(),name='admindelete'),
    path('department/',department),
    path('doctor/',doctor),
    path('signup/',signUpView),
    path('verify/<auth_token>',verify),
    path('appointment/',appointments),
    path('appointmentlist/',appointment_list)

]
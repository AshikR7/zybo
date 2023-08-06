from django.urls import path
from .views import *
urlpatterns=[
    path('superregister/',superRegister),
    path('superlogin/',superLogin),
    path('superprofile/',superProfile),
    path('adminregister/',adminRegister),
    path('verify/<auth_token>',verify),
    path('adminlogin/',adminLogin),
    path('adminprofile/',adminProfile),
    path('adminlist/',adminList.as_view(),name='adminlist'),
    path('adminupdate/<pk>',adminUpdate.as_view(),name='adminupdate'),
    path('admindelete/<pk>',AdminDelete.as_view(),name='admindelete'),
    path('department/',department),
    path('doctor/',doctor),
    path('signup/',signUpView),
    path('userlogin/',userLogin),
    path('appointment/',appointments,),
    path('appointmentlist/',appointment_list),
    path('singleappointment/<int:id>',singleAppointmentList),
    path('changestatus/<int:id>',statusChange),


]
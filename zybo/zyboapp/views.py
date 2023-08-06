from django.shortcuts import render
import uuid
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import logout
from zybo.settings import EMAIL_HOST_USER

def superProfile(request):
    return render(request,'superProfile.html')
def adminProfile(request):
    return render(request,'adminProfile.html')

def superRegister(request):
    if request.method=='POST':
        a=superRegisterForm(request.POST)
        if a.is_valid():
            us=a.cleaned_data["superadmin"]
            em=a.cleaned_data["email"]
            ps=a.cleaned_data["password"]
            cp=a.cleaned_data["conpassword"]
            if ps==cp:
                b=superAdminModel(superadmin=us,email=em,password=ps)
                b.save()
                return redirect(superLogin)
            else:
                return HttpResponse("password doesn't match")
        else:
            return HttpResponse("fail")
    return render(request,'superregister.html')

def superLogin(request):
    if request.method=='POST':
        a=superLoginForm(request.POST)
        if a.is_valid():
            em=a.cleaned_data["email"]
            ps=a.cleaned_data["password"]
            b=superAdminModel.objects.all()
            for i in b:
                if em==i.email and ps==i.password:
                    return redirect(superProfile)
            else:
                return HttpResponse("login Failed")
    return render(request,'superlogin.html')

def adminRegister(request):
    if request.method=='POST':
        a=adminRegisterForm(request.POST)
        if a.is_valid():
            us=a.cleaned_data["admin"]
            em=a.cleaned_data["email"]
            ps=a.cleaned_data["password"]
            cp=a.cleaned_data["conpassword"]
            if ps==cp:
                b=adminModel(admin=us,email=em,password=ps)
                b.save()
                return redirect(superProfile)
            else:
                return HttpResponse("password doesn't match")
        else:
            return HttpResponse("fail")
    return render(request,'adminRegister.html')
def adminLogin(request):
    if request.method=='POST':
        a=superLoginForm(request.POST)
        if a.is_valid():
            em=a.cleaned_data["email"]
            ps=a.cleaned_data["password"]
            b=adminModel.objects.all()
            for i in b:
                if em==i.email and ps==i.password:
                    return redirect(adminProfile)
            else:
                return HttpResponse("login Failed")
    return render(request,'adminLogin.html')


class adminList(generic.ListView):
    model = adminModel
    template_name = 'adminList.html'
    def get(self,request):
        a = self.model.objects.all()
        return render(request,self.template_name,{'a':a})
class adminUpdate(generic.UpdateView):
    model = adminModel
    template_name = 'adminUpdate.html'
    fields = ['admin','email']
    success_url = reverse_lazy('adminlist')

class AdminDelete(generic.DeleteView):
    model = adminModel
    template_name = 'adminDelete.html'
    success_url = reverse_lazy('adminlist')

def department(request):
    if request.method=='POST':
        a=departmentForm(request.POST)
        if a.is_valid():
            dp = a.cleaned_data['department']
            b=departmentModel(department=dp)
            b.save()
            return redirect(adminProfile)
    return render(request,'department.html')
def doctor(request):
    depart = departmentModel.objects.all()
    if request.method=='POST':
        a=doctorForm(request.POST,request.FILES)
        if a.is_valid():
            nm=a.cleaned_data['name']
            dp=a.cleaned_data['department']
            ph=a.cleaned_data['photo']
            ql=a.cleaned_data['qualification']
            b=doctorModel(name=nm,department=dp,photo=ph,qualification=ql)
            b.save()
            return redirect(adminProfile)
    return render(request,'doctor.html',{'depart':depart})

class doctorlist(generic.ListView):
    model = doctorModel
    template_name = 'doctor.html'
    def get(self,request):
        a = self.model.objects.all()
        return render(request,self.template_name,{'b':a})

def signUpView(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email = request.POST.get('email')
        password=request.POST.get('password')
        if User.objects.filter(username=username).first():
            messages.success(request,'username is already taken')
            return redirect(signUpView)

        if User.objects.filter(email=email).first():
            messages.success(request, 'email is already taken')
            return redirect(signUpView)
        user_obj=User(username=username,email=email)
        user_obj.set_password(password)
        user_obj.save()
        auth_token=str(uuid.uuid4())
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        sendMailSignUp(email,auth_token)
        return render(request,'success.html')
    return render(request,'userSignUp.html')
def sendMailSignUp(email,auth_token):
    subject="your account has been varified"
    message=f'click the link to verify your account http://127.0.0.1:8000/zybo/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)
def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(userLogin)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(userLogin)
    else:
        messages.success(request,'user not found')
        return redirect(userLogin)

def userLogin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        request.session['username']=username
        user_obj= User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'user not found')
            return redirect(userLogin)
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your email')
            return redirect(userLogin)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(userLogin)
        return redirect(appointments)
    return render(request,'userLogin.html')


def appointments(request):
    depart = departmentModel.objects.all()
    doctor = doctorModel.objects.all()
    appointmentList=appointmentsModel.objects.all()
    apDate=[]
    apTime=[]
    for i in appointmentList:
        adt = i.date
        apDate.append(adt)
        atm=i.time
        apTime.append(atm)
    if request.method=='POST':
        a=appointmentsForm(request.POST,request.FILES)
        if a.is_valid():
            nm=a.cleaned_data['name']
            em=a.cleaned_data['email']
            ph=a.cleaned_data['phone']
            pl=a.cleaned_data['place']
            dt = a.cleaned_data['date']
            tm = a.cleaned_data['time']
            dp = a.cleaned_data['department']
            do = a.cleaned_data['doctor']
            if dt in apDate and tm in apTime:
                return HttpResponse("please select another Date or Time")

            b=appointmentsModel(name=nm,email=em,phone=ph,place=pl,date=dt,time=tm,department=dp,doctor=do)
            b.save()
            status(em)
            return HttpResponse("success")
    return render(request,'appointment.html',{'depart':depart,'doctor':doctor},)

def status(email):
    subject="Status Upadate"
    message=f'Current status is pending, please wait for new mail from Admin'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)


def appointment_list(request):
    list=appointmentsModel.objects.all()
    return render(request,'appointmentlist.html',{'appointment':list})

def singleAppointmentList(request,id):
    list = appointmentsModel.objects.filter(id=id)
    return render(request, 'singleAppointmentList.html', {'appointment': list})

def statusChange(request,id):
    a=appointmentsModel.objects.get(id=id)
    em=a.email
    currentStatus=a.status
    if request.method=='POST':
        a.status=request.POST.get('status')
        s=a.status
        a.save()
        newStatus(em,s)
        return redirect(appointment_list)
    return render(request,'changeStatus.html',{'new':a,'current':currentStatus,})

def newStatus(email,s):
    subject="Status Upadate"
    message=f'Status is changed to {s}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

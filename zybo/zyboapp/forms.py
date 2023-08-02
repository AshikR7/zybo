from django import forms
class superRegisterForm(forms.Form):
    superadmin=forms.CharField(max_length=30)
    email=forms.EmailField()
    password=forms.CharField(max_length=30)
    conpassword=forms.CharField(max_length=30)

class superLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30)

class adminRegisterForm(forms.Form):
    admin=forms.CharField(max_length=30)
    email=forms.EmailField()
    password=forms.CharField(max_length=30)
    conpassword=forms.CharField(max_length=30)

class adminLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=30)

class departmentForm(forms.Form):
    department = forms.CharField(max_length=30)
class doctorForm(forms.Form):
    name = forms.CharField(max_length=30)
    department = forms.CharField(max_length=30)
    photo = forms.ImageField()
    qualification = forms.CharField(max_length=30)

class appointmentsForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone = forms.IntegerField()
    place = forms.CharField(max_length=30)
    date = forms.DateField()
    time = forms.TimeField()
    department = forms.CharField(max_length=30)
    doctor = forms.CharField(max_length=30)
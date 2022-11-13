from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class FarmersForm(ModelForm):
    class Meta:
        model = Farmer
        fields = '__all__'


class BuyersForm(ModelForm):
    class Meta:
        model = Buyer
        fields = '__all__'
        
        
        
class CountyForm(ModelForm):
    class Meta:
        model = County
        fields = '__all__'
        
        
class CountyAgriForm(ModelForm):
    class Meta:
        model = CountyAgriOfficer
        exclude = ['invoice_no', 'invoice_id']
        


class CentreManagerForm(ModelForm):
    class Meta:
        model = CentreManager
        fields = '__all__'
        
        
class ProduceForm(ModelForm):
    class Meta:
        model = Produce
        fields = '__all__'
        
class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        
        
        
class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        exclude = ['invoice_no', 'invoice_id']
        
    
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )





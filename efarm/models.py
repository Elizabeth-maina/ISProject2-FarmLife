from email.policy import default
from itertools import count
from unicodedata import name
from django.urls import reverse
from django.db import models
import uuid
from django.contrib.auth.models import User

class County(models.Model):
    name = models.CharField(max_length=254)
    email = models.EmailField()
    adress = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)
    code = models.IntegerField(null=False)

    def __str__(self):
        return self.name

class Centre(models.Model):
    name = models.CharField(max_length=254)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    phone = models.CharField(max_length=254)
    
    def __str__(self):
        return self.name   
    

class Farmer(models.Model):
    gender_choice = (
        ('male', 'male',),
        ('female', 'female'),
        ('other', 'other')
    )
    first_name = models.CharField(max_length=254)
    second_name = models.CharField(max_length=254)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=254, choices=gender_choice)
    email = models.EmailField()
    adress = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name

    @property
    def get_name(self):
        full_name = self.first_name + ' ' + self.second_name

        return full_name
class CentreManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254)
    second_name = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    centre = models.ForeignKey(Centre, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
       
    @property
    def get_name(self):
        full_name = self.first_name + ' ' + self.second_name

        return full_name
    
class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254)
    second_name = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
       
    @property
    def get_name(self):
        full_name = self.first_name + ' ' + self.second_name

        return full_name
    
class CountyAgriOfficer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=254)
    second_name = models.CharField(max_length=254)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    county = models.ForeignKey(County, on_delete=models.CASCADE)


    def __str__(self):
        return self.first_name
    
    @property
    def get_name(self):
        full_name = self.first_name + ' ' + self.second_name

        return full_name


class Produce(models.Model):
    name = models.CharField(max_length=254)
    generic_name = models.CharField(max_length=254)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=7)
    quantity = models.DecimalField(decimal_places=2, max_digits=7)
    image = models.ImageField(upload_to='produce', null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Invoice(models.Model):
    status_options = (
        ('Paid', 'Paid'),
        ('Not Paid', 'Not Paid'),
    )
    payment_choices = (
        ('Cash', 'Cash'),
        ('Bank', 'Bank'),
        ('Mpesa', 'Mpesa'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True, null=True)
    invoice_no = models.AutoField(primary_key=True)
    invoice_id = models.UUIDField(default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    discount = models.DecimalField(decimal_places=2, max_digits=10)
    VAT = models.DecimalField(decimal_places=2, max_digits=10, default=16)
    payment_method = models.CharField(max_length=254, choices=payment_choices)
    status = models.CharField(max_length=254, choices=status_options)
    
    @property
    def get_total(self):
        total = (self.price*self.quantity)-(self.discount+(self.price*self.quantity*(self.VAT/100)))
        return total
    
class Blog(models.Model):
    title = models.CharField(max_length=254,null=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='blogs', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        



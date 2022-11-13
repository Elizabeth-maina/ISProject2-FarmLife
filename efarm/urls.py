from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('farmers_list/', FarmersList, name='farmers'),
    path("add_farmer/", addFarmer, name='add_farmer'),
    path('produce_list/', ProduceList, name='produce'),
    path("add_produce/", addProduce, name='add_produce'),
    path('county_list/', CountyList, name='counties'),
    path('add_county/', addCounty, name='add_county'),
    path('centre_manager_list/', CentreManagerList, name='centre_managers'),
    path('add_centre_manager/', addCentreManager, name='add_centre_manager'),
    path('buyers_list/', BuyersList, name='buyers'),
    path('add_buyers/', addBuyer, name='add_buyer'),
    path('invoices_list/', InvoiceList, name='invoices'),
    path('add_invoice/', addInvoice, name='add_invoice'),
    path('blogs/', BlogList, name='blogs'),
    path('add_blog/', addBlog, name='add_blog'),
    path('login/', Login, name='login'),
    path('logout/', logoutUser, name="logout"),



]
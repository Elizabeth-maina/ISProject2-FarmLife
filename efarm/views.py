from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from django.utils import timezone
from django.contrib import messages
from .models import *
from .forms import *
from .filters import *
from .utils import *
from django.http import JsonResponse
import json
from .decorators import allowed_users


# Create your views here.

# login
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('blog')
        else:
            messages.info(request, 'Incorrect Username or Password!')
    context = {}
    return render(request, 'login.html', context)

# logout
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    farmers = Farmer.objects.all()
    total_farmers = farmers.count()
    produce = Produce.objects.all()
    total_produce = produce.count()
    buyers = Buyer.objects.all()
    total_buyers = buyers.count()
    centre_managers = CentreManager.objects.all()
    centres = Centre.objects.all()
    for centre in centres:
        print(centre.name)

    total_centres = Centre.objects.all().count()
    total_centre_managers = centre_managers.count()
    
    #sales
    sales_today = Invoice.objects.filter(date_created__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_created__lte=timezone.now().replace(hour=23, minute=59, second=59)).count()
    sales_this_mon = Invoice.objects.filter(
        date_created__month=current_month)
    cash = Invoice.objects.filter(payment_method='Cash', date_created__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_created__lte=timezone.now().replace(hour=23, minute=59, second=59))
    cash_received = sum([i.get_total for i in cash])

    mpesa = Invoice.objects.filter(payment_method='Mpesa', date_created__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_created__lte=timezone.now().replace(hour=23, minute=59, second=59))
    mpesa_received = sum([i.get_total for i in mpesa])

    bank = Invoice.objects.filter(payment_method='Bank', date_created__gte=timezone.now().replace(
        hour=0, minute=0, second=0), date_created__lte=timezone.now().replace(hour=23, minute=59, second=59))
    bank_received = sum([i.get_total for i in bank])
    daily_total = cash_received + mpesa_received + bank_received
    
    mon_cash = Invoice.objects.filter(payment_method='Cash',date_created__month=current_month)
    mon_cash_received = sum([i.get_total for i in mon_cash])

    mon_mpesa = Invoice.objects.filter(payment_method='Mpesa', date_created__month=current_month)
    mon_mpesa_received = sum([i.get_total for i in mon_mpesa])

    mon_bank = Invoice.objects.filter(payment_method='Bank', date_created__month=current_month)
    mon_bank_received = sum([i.get_total for i in mon_bank])
    mon_total = mon_cash_received + mon_mpesa_received + mon_bank_received
    
    totals = Invoice.objects.filter(date_created__year=current_year)
    annual_total = sum([i.get_total for i in totals])
    
    context = {'total_farmers': total_farmers,
               'total_produce': total_produce,
               'total_buyers': total_buyers,
               'total_centre_managers': total_centre_managers,
               'sales_today': sales_today,
               'sales_this_mon': sales_this_mon,  
               'cash_received': cash_received,
               'mpesa_received': mpesa_received,
               'bank_received': bank_received,
               'daily_total': daily_total,
               'mon_cash_received': mon_cash_received,
               'mon_mpesa_received': mon_mpesa_received,
               'mon_bank_received': mon_bank_received,
               'mon_total': mon_total,
               'annual_total':annual_total,
               'group': group,
               'centres':centres,
               "total_centres":total_centres,
               "produce": produce
               
               }
    return render(request, 'index.html', context)


# Customers
@login_required(login_url='login')
def FarmersList(request):
    farmers = Farmer.objects.all()

    myFilter = FarmersFilter(request.GET, queryset=farmers)
    farmers = myFilter.qs

    paginator = Paginator(farmers, 10)
    page_number = request.GET.get('page', 1)
    farmer_obj = paginator.get_page(page_number)
    context = {'farmers': farmers,
               'farmer_obj': farmer_obj, 'myFilter': myFilter}
    return render(request, 'farmers/farmers_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['center-manager'])
def addFarmer(request):
    form = FarmersForm()
    if request.method == 'POST':
        form = FarmersForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('farmers')

    context = {"form": form}
    return render(request, 'farmers/add_farmers.html', context)

@login_required(login_url='login')
def ProduceList(request):
    farmers = Produce.objects.all()

    myFilter = ProduceFilter(request.GET, queryset=farmers)
    produce = myFilter.qs

    paginator = Paginator(farmers, 10)
    page_number = request.GET.get('page', 1)
    produce_obj = paginator.get_page(page_number)
    context = {'produce': produce,
               'produce_obj': produce_obj, 'myFilter': myFilter}
    return render(request, 'produce/produce_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['center-manager'])
def addProduce(request):
    form = ProduceForm()
    if request.method == 'POST':
        form = ProduceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('produce')

    context = {'form':form}
    return render(request, 'produce/add_produce.html', context)

@login_required(login_url='login')
def CountyList(request):
    counties = County.objects.all()

    myFilter = CountyFilter(request.GET, queryset=counties)
    county = myFilter.qs

    paginator = Paginator(county, 10)
    page_number = request.GET.get('page', 1)
    county_obj = paginator.get_page(page_number)
    context = {'county': county,
               'county_obj': county_obj, 'myFilter': myFilter}
    return render(request, 'county/county_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['center-manager'])
def addCounty(request):
    form = CountyForm()
    if request.method == 'POST':
        form = CountyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('counties')

    context = {'form':form}
    return render(request, 'county/add_county.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['county-agri-officer'])
def CentreManagerList(request):
    centre_manager = CentreManager.objects.all()

    myFilter = CentreManagerFilter(request.GET, queryset=centre_manager)
    centre_manager = myFilter.qs

    paginator = Paginator(centre_manager, 10)
    page_number = request.GET.get('page', 1)
    centre_manager_obj = paginator.get_page(page_number)
    context = {'centre_manager': centre_manager,
               'centre_manager_obj': centre_manager_obj, 'myFilter': myFilter}
    return render(request, 'users/centre_manager_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['county-agri-officer'])
def addCentreManager(request):
    form = CentreManagerForm()
    if request.method == 'POST':
        form = CentreManagerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('centre_managers')

    context = {'form':form}
    return render(request, 'users/add_centre_manager.html', context)

@login_required(login_url='login')
def BuyersList(request):
    buyers = Buyer.objects.all()

    myFilter = BuyersFilter(request.GET, queryset=buyers)
    buyers = myFilter.qs

    paginator = Paginator(buyers, 10)
    page_number = request.GET.get('page', 1)
    buyers_obj = paginator.get_page(page_number)
    context = {'buyers': buyers,
               'buyers_obj': buyers_obj, 'myFilter': myFilter}
    return render(request, 'users/buyers_list.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['centre-manager'])
def addBuyer(request):
    form = BuyersForm()
    if request.method == 'POST':
        form = BuyersForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('buyers')

    context = {"form": form}
    return render(request, 'users/add_buyers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['center-manager'])
def addInvoice(request):
    form = InvoiceForm()
    if request.method == 'POST':
        form = InvoiceForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('invoices')

    context = {"form": form}
    return render(request, 'payments/add_invoice.html', context)


@login_required(login_url='login')
def InvoiceList(request):
    invoices = Invoice.objects.all()

    myFilter = InvoiceFilter(request.GET, queryset=invoices)
    invoices = myFilter.qs
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page', 1)
    invoices_obj = paginator.get_page(page_number)
  
    context = {'invoices': invoices,
               'invoices_obj': invoices_obj, 'myFilter': myFilter}
    return render(request, 'payments/invoices_list.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['center-manager'])
def addBlog(request):
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blogs')

    context = {"form": form}
    return render(request, 'farmers/add_blogs.html', context)

@login_required(login_url='login')
def BlogList(request):
    blogs = Blog.objects.all()

    myFilter = BlogFilter(request.GET, queryset=blogs)
    blogs = myFilter.qs
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page', 1)
    blogs_obj = paginator.get_page(page_number)
  
    context = {'blogs': blogs,
               'blogs_obj': blogs_obj, 'myFilter': myFilter}
    return render(request, 'farmers/blogs_list.html', context)






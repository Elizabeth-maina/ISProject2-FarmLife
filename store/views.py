from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from .models import *
import json
import requests
from django.contrib import messages
import uuid
from .utils import *
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users, admin_only, unauthenticated_user
from django.core.paginator import Paginator
from efarm.filters import *

@login_required(login_url='login')
def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    
    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    products = Produce.objects.all()
    myFilter = ProduceFilter(request.GET, queryset=products)
    products = myFilter.qs


    context = {"products": products, "myFilter":myFilter, "cartItems": cartItems, "order": order, "group": group}
    return render(request, "store/store.html", context)

@login_required(login_url='login')
def cart(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    customer = request.user
    product = Produce.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add" or action == "buyNow":
        orderItem.quantity += 1
    elif action == "remove":
        orderItem.quantity -= 1

    orderItem.save()

    total = order.get_cart_items
    totalValue = float(orderItem.get_total)
    quantity = orderItem.quantity

    orderTotalValue = float(order.get_cart_total)

    if orderItem.quantity <= 0:
        orderItem.delete()
        totalValue = 0
        quantity = 0

    data = {
        "cartTotal": total,
        "productQuantity": quantity,
        "orderItemTotalValue": totalValue,
        "orderTotalValue": orderTotalValue,
    }

    return JsonResponse(
        data=data,
        safe=False,
    )


def processOrder(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        uname = data["form"]["username"]
        email = data["form"]["email"]
        password = data["form"]["password"]

        errors = []
        if User.objects.filter(username=uname).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email is already in use.")

        errCount = len(errors)

        if errCount > 0:
            return JsonResponse({"errors": errors}, safe=False,status=403)

        customer, order = guestOrder(request, data)

        if customer.user is not None:
            login(request, customer.user)
        else:
            print("is none")

    total = float(data["form"]["total"])

    if total != float(order.get_cart_total):
        err = {"err": "Your order total value does not match."}
        return JsonResponse({"errors": [err]}, safe=False, status=403)

    order.save()

    return JsonResponse({"id": order.id}, safe=False)


def confirmPayment(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        transaction_id = str(uuid.uuid4())
        order.transaction_id = transaction_id
        order.paypalTransactionId = data["paypalTxId"]
        order.complete = True
        order.save()

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
    
def mpesaPaymnet(request):
    user = request.user
    amount = 1000
    phone_number = 254725792973
    try:
        mpesa = requests.post("http://127.0.0.1:8000/mpesa/submit/", data={"phone_number": phone_number,"amount": amount}) 
        messages.success(request, "Check Your Phone and Input your Mpesa PIN to make payment.")
        response = HttpResponseRedirect('checkout')
        response.delete_cookie("cart")
    except:
        messages.error("Something went wrong")
    
    context = {}
 
    return redirect('checkout')


def profile(request):  # /profile
    data = cartData(request)

    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]
    user = request.user
    orders = Order.objects.filter(customer=user)
    invoices = Invoice.objects.filter(customer=user)
    print(invoices)

    context = {"items": items, "order": order, "cartItems": cartItems, "user": user, 'orders':orders, 'invoices': invoices,}
    return render(request, "store/profile.html", context)


def updPersonalInfo(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        fName = data["fName"]
        lName = data["lName"]
        user = User.objects.get(username=request.user.username)
        user.first_name = fName
        user.last_name = lName
        user.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def updEmail(request):
    data = json.loads(request.body)
    if request.user.is_authenticated:
        email = data["email"]
        user = User.objects.get(username=request.user.username)
        customer = User.objects.get(user=user)
        user.email = email
        customer.email = email
        user.save()
        customer.save()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
    
@login_required(login_url='login')
def blog(request):
    blogs = Blog.objects.all()
    context = {'blogs':blogs}
    return render(request, "blog/index.html", context)
    
    
    

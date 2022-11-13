from django.urls import path

from . import views

urlpatterns = [
    
    path("store", views.store, name="restaurant"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("process_order_mpesa/", views.mpesaPaymnet, name="process_mpesa"),
    path("confirm_payment/", views.confirmPayment, name="confirm_payment"),
    path("profile/", views.profile, name="profile"),
    path("upd_personal_info/", views.updPersonalInfo, name="updPersonalInfo"),
    path("upd_email/", views.updEmail, name="updEmail"),
    path("", views.blog, name="blog"),

]
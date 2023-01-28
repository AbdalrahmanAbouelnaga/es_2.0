from django.urls import path
from . import views

urlpatterns = [
    path('checkout/stripe/',views.checkout),
    path('checkout/paymob/',views.paymob_payment)
]
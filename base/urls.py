from django.urls import path
from . import views

urlpatterns = [
    path('initialize-payment/', views.make_payment, name='initialize-payment'),
    path('get-transaction/',views.get_transaction,name='get-transaction'),
] 
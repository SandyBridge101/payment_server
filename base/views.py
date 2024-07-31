from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from .models import *

# Create your views here.

headers = {
    'Authorization': 'Bearer sk_live_9569be8a853e988f942f96367167bb7c07b35707',
    'Content-Type': 'application/json',
}


@csrf_exempt
def make_payment(request):
    url='https://api.paystack.co/transaction/initialize'
    return_response={}

    if request.method=="POST":
        print(request.body)
        request_data=json.loads(request.body)
        email=request_data.get("email")
        amount=request_data.get('amount')
        order=request_data.get('order')
        body={
            'email':email,
            'amount':amount,
            'order':order
        }

        payment_response=requests.post(url,json=body,headers=headers)

        if payment_response.status_code>=200:
            payment_response_body=payment_response.json()['data']
            print(payment_response_body)
            payment,created=PaymentOrder.objects.get_or_create(
                order=order,
                defaults={
                    'order':order,
                    'email':email,
                    'amount':amount,
                    'access_code':payment_response_body['access_code'],
                    'reference':payment_response_body['reference'],
                    'auth_url':payment_response_body['authorization_url'],
                }
            )

            if not created:
                payment.order=order
                payment.email=email
                payment.amount=amount
                payment.access_code=payment_response_body['access_code']
                payment.reference=payment_response_body['reference']
                payment.auth_url=payment_response_body['authorization_url']

            payment.save()

            return_response={
                'message':'Successful',
                'url':payment_response_body['authorization_url']
            }
    else:
        return_response={
            'message':'Payment Operation was not successful'
        }
        
    return JsonResponse(return_response)


@csrf_exempt
def get_transaction(request):
    if request.method=='POST':
        print(request.body)
        request_data=json.loads(request.body)
        order=request_data.get('order')

        try:
            payment_order=PaymentOrder.objects.get(order=order)
        except PaymentOrder.DoesNotExist:
            return JsonResponse({'message':'Order data not found'})
        except Exception as e:
            return JsonResponse({'message':'Error retrieving data'})
        
        reference=payment_order.reference
        
        url=f'https://api.paystack.co/transaction/verify/{reference}'

        transaction_response=requests.get(url,headers=headers)

        if transaction_response.status_code>=200:
            return JsonResponse(transaction_response.json())
        else:
            return JsonResponse({'message':'Could not get transaction data'})


from django.db import models

# Create your models here.

class PaymentOrder(models.Model):
    order=models.IntegerField()
    email=models.EmailField()
    amount=models.DecimalField(max_digits=6,decimal_places=2)
    access_code=models.CharField(max_length=1000)
    reference=models.CharField(max_length=1000)
    auth_url=models.CharField(max_length=10000)
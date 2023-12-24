import uuid
from django.db import models
from Course.models import *
from UserAuth.models import *
from django.utils import timezone

class Transaction(models.Model):
    transaction_id = models.CharField(primary_key=True, max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    resi = models.CharField(max_length=100, null=True)
    progress = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    snap_token = models.CharField(max_length=100, null=True)
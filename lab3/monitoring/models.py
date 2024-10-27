from django.db import models
from datetime import datetime 
from django.contrib.auth.models import User

class Threat(models.Model):
    threat_name = models.CharField(max_length=60, null=False)
    company_name = models.CharField(max_length=60, null=False)
    short_description = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    status = models.CharField(max_length=30, null=False)
    img_url = models.CharField(max_length=255, null=False)
    price = models.IntegerField(null=False)
    detections = models.IntegerField(null=False)

    class Meta:
        managed = True
        db_table = 'threats'

class Request(models.Model):
    status = models.CharField(max_length=30, null=False, default='draft')
    created_at = models.DateTimeField(null=False, default=datetime.now())
    formed_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    moderator = models.ForeignKey(User,on_delete=models.CASCADE, null=True,related_name='moderator')
    final_price = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'requests'

class RequestThreat(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='request_threats')
    threat = models.ForeignKey(Threat, on_delete=models.CASCADE)
    price = models.BigIntegerField(null=True)
    comment = models.TextField(null=True)

    class Meta:
        managed = True
        db_table = 'requests_threats'
        constraints = [
            models.UniqueConstraint(fields=['request', 'threat'], name='unique_request_threat')
        ]
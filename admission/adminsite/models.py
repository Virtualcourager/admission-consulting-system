from django.db import models
from information.models import MajorInfo
from users.models import UserProfile, Province
# Create your models here.

class HistoryInfo(models.Model):
    major = models.ForeignKey(MajorInfo , on_delete=models.CASCADE,related_name='history_major')
    rank = models.IntegerField(null=True,blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE,related_name='history_province')

class BorderlinePredict(models.Model):
    major = models.ForeignKey(MajorInfo, on_delete=models.CASCADE, related_name='predict_major')
    lowscore = models.IntegerField(null=True, blank=True)
    highscore = models.IntegerField(null=True, blank=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='predict_province')
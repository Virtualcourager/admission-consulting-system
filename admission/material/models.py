from django.db import models
from django.contrib.auth.models import User
import time

# Create your models here.

def get_upload_file_name(filename):
    return "uploaded_files/%s_%s" % (str(time.time()).replace('.','_'),filename)

class ConsultMaterial(models.Model):
    name = models.CharField(max_length=100)
    province_id = models.SmallIntegerField()
    file_name = models.CharField(max_length=25, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

from django.db import models
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Province(models.Model):
    province = models.CharField(max_length=5)

    def __str__(self):
        return self.province


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telephone = models.CharField('Telephone', max_length=50, blank=True)
    province= models.ForeignKey('Province',on_delete=models.CASCADE, blank=True, default=1 )
    place = models.CharField('place', max_length=50, blank=True)
    class Meta:
        verbose_name = 'User Profile'
    def __str__(self):
        return self.user.__str__()
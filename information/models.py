from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MajorInfo(models.Model):
    major_name = models.CharField(max_length=30)
    sciorart = models.ForeignKey('SciorArt', on_delete=models.CASCADE)
    is_international=models.BooleanField()
    def __str__(self):
        return self.major_name
class SciorArt(models.Model):
    SciorArt=models.CharField(max_length=2)
    def __str__(self):
        return self.SciorArt

class StuInfo(models.Model):
    id = models.AutoField(primary_key=True)                         #自增的id，作为主键
    name = models.CharField(max_length=20)                          #姓名
    testnum = models.CharField(max_length=14)                       #考生号，通常最多14位
    score = models.PositiveSmallIntegerField()                      #小整数，存储最大32767
    rank = models.PositiveSmallIntegerField()                       #排名，目前可存储最大32767
    tele = models.CharField(max_length=20)                          #电话
    high_school = models.CharField(max_length=30)                   #毕业学校
    sciorart = models.ForeignKey('SciorArt',on_delete=models.CASCADE)
    major1 = models.ForeignKey('MajorInfo',on_delete=models.CASCADE,null=True,blank=True,related_name='major1')
    major2 = models.ForeignKey('MajorInfo', on_delete=models.CASCADE,null=True,blank=True,related_name='major2')
    major3 = models.ForeignKey('MajorInfo', on_delete=models.CASCADE,null=True,blank=True,related_name='major3')
    is_international = models.BooleanField(default=False)
    application_rank = models.PositiveSmallIntegerField()
    staff = models.ForeignKey(User,on_delete=models.CASCADE,null=True,)     #自动生成，无需填写
    province = models.ForeignKey('users.Province',null=True,on_delete=models.CASCADE)
    place = models.CharField(max_length=30,default="NULL")        #自动生成，无需填写
    tip = models.CharField(max_length=200,null=True,blank=True)   #由后台管理员填写
    date = models.DateField(auto_now_add=True)
    time  = models.TimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural ='entries'


class RankPredict(models.Model):
    province = models.ForeignKey('users.Province',on_delete=models.CASCADE)
    sciorart = models.ForeignKey('SciorArt', on_delete=models.CASCADE,default=1)
    score = models.PositiveSmallIntegerField()
    highrank = models.PositiveSmallIntegerField(null=True,blank=True)
    lowrank = models.PositiveSmallIntegerField(null=True,blank=True)
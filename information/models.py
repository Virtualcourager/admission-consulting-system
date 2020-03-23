from django.db import models

# Create your models here.
class MajorInfo(models.Model):
    major_name = models.CharField(max_length=5)

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
    major = models.ForeignKey('MajorInfo',on_delete=models.CASCADE)
    application_rank = models.PositiveSmallIntegerField()
    staff_id = models.PositiveIntegerField(default=0)              #自动生成，无需填写
    place = models.CharField(max_length=30,default="NULL")        #自动生成，无需填写
    tip = models.CharField(max_length=200,null=True,blank=True)   #由后台管理员填写
    date = models.DateField(auto_now_add=True)
    time  = models.TimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural ='entries'

class ProvinceInfo(models.Model):
    province_name = models.CharField(max_length=10)
    def __str__(self):
        return self.province_name

class RankPredict(models.Model):
    province = models.ForeignKey('ProvinceInfo',on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()
    highrank = models.PositiveSmallIntegerField()
    lowrank = models.PositiveSmallIntegerField()
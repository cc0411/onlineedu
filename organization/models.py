from django.db import models
from datetime import  datetime
# Create your models here.


class CityDict(models.Model):
    name = models.CharField(max_length=12,verbose_name=u'城市')
    desc = models.CharField(max_length=100,verbose_name=u'描述')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=30,verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'描述')
    click_nums = models.SmallIntegerField(default=0,verbose_name=u'点击数')
    fav_nums = models.SmallIntegerField(default=0,verbose_name=u'收藏数')
    image = models.ImageField(verbose_name=u'封面图',max_length=100,upload_to='org/%Y/%m')
    address = models.CharField(max_length=150,verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict,verbose_name='城市')
    add_time = models.DateTimeField(default=datetime.now)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name=u'机构')
    name = models.CharField(max_length=20,verbose_name="姓名")
    work_years = models.SmallIntegerField(verbose_name=u'工作年限',)
    work_company = models.CharField(max_length=50,verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50,verbose_name=u'职位')
    points = models.CharField(max_length=100,verbose_name=u'教学特点')
    click_nums = models.SmallIntegerField(default=0,verbose_name=u'点击数')
    fav_nums= models.SmallIntegerField(default=0,verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'讲师'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name









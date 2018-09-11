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

    category = models.SmallIntegerField(choices=((1,'培训机构'),(2,'高校'),(3,'个人')),default=1,verbose_name=u'机构类别')
    click_nums = models.SmallIntegerField(default=0,verbose_name=u'点击数')
    fav_nums = models.SmallIntegerField(default=0,verbose_name=u'收藏数')
    image = models.ImageField(verbose_name=u'封面图',max_length=100,upload_to='org/%Y/%m')
    address = models.CharField(max_length=150,verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict,verbose_name='城市')
    add_time = models.DateTimeField(default=datetime.now)
    # 当学生点击学习课程，找到所属机构，学习人数加1
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    # 当发布课程就加1
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,verbose_name=u'机构')
    image = models.ImageField(
        default='',
        upload_to="teacher/%Y/%m",
        verbose_name=u"头像",
        max_length=100)
    name = models.CharField(max_length=20,verbose_name="姓名")
    work_years = models.SmallIntegerField(verbose_name=u'工作年限',)
    age = models.SmallIntegerField(verbose_name=u'年龄',default=18 )
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









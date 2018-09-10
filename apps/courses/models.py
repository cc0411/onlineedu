from django.db import models
from datetime import  datetime
from organization.models import CourseOrg
# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=30,verbose_name=u'课程名')
    desc = models.CharField(max_length=300,verbose_name=u'描述')
    detail = models.TextField(verbose_name=u'课程详情')
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", null=True, blank=True)
    degree = models.SmallIntegerField(default=1,choices=((1,'初级'),(2,'中级'),(3,'高级')),verbose_name=u'课程难度')
    learn_time = models.IntegerField(default=0,verbose_name=u'学习时长/min')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏数')
    category = models.CharField(max_length=20, default=u"", verbose_name=u"课程类别")
    image = models.ImageField(upload_to='course/%Y/%m',verbose_name=u'课程图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    tag = models.CharField(max_length=15, verbose_name=u"课程标签", default=u"")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')
    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name
    #获取课程所有章节
    def get_zj_nums(self):
        return self.lesson_set.all().count()
    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=20,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节')
    name = models.CharField(max_length=20,verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'视频'
        verbose_name_plural  = verbose_name
    def __str__(self):
        return self.name

class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    name = models.CharField(max_length=30,verbose_name=u'课件名')
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name=u'课件文件',max_length=100)
    add_time = models.DateTimeField(verbose_name=u'添加时间',default=datetime.now)
    class Meta:
        verbose_name = u'课件'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

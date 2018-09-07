from django.db import models
from datetime import  datetime

# Create your models here.


from users.models import UserProfile
from courses.models import Course


class UserAsk(models.Model):
    name = models.CharField(max_length=30,verbose_name=u'姓名')
    mobile = models.CharField(max_length=11,verbose_name=u'手机号')
    course_name = models.CharField(max_length=50,verbose_name=u'咨询课程')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name
    def  __str__(self):
        return self.name


class CourseComents(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    comments = models.CharField(max_length=300,verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{0}-{1}'.format(self.user.username,self.course.name)

class  Userfav(models.Model):
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    fav_id = models.IntegerField(default=0)
    fav_type = models.SmallIntegerField(default=1,verbose_name=u'收藏类型',choices=((1,u'课程'),(2,u'机构'),(3,'讲师')))
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user.username

class UserMessage(models.Model):
    user = models.IntegerField(default=0,verbose_name=u'接收用户')
    message = models.CharField(max_length=100,verbose_name=u'内容')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.user

class  UserCourse(models.Model):
    course = models.ForeignKey(Course,verbose_name=u'课程')
    user = models.ForeignKey(UserProfile,verbose_name=u'用户')
    add_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name




















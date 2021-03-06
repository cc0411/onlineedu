from datetime import  datetime


from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(max_length=12,verbose_name=u'昵称',default='')
    birthday = models.DateTimeField(verbose_name=u'生日',null=True,blank=True)
    gender = models.CharField(verbose_name=u'性别',max_length=11,choices=(('man','男'),('woman','女')),default='man')
    address = models.CharField(max_length=100,blank=True,null=True,verbose_name=u'地址')
    mobile = models.CharField(max_length=11,null=True,blank=True,verbose_name=u'手机号')
    image = models.ImageField(max_length=100,upload_to='images/%Y/%m',default='images/default.png')
    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=12,verbose_name=u'验证码')
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(max_length=12,choices=(("register",'注册'),('forget','忘记密码'),("update_email","修改邮箱")))
    send_time = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{0}-{1}'.format(self.email,self.code)


class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m',max_length=100,verbose_name=u'轮播图')
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    index = models.SmallIntegerField(default=100,verbose_name=u'索引')
    add_time  = models.DateTimeField(default=datetime.now)
    class Meta:
        verbose_name =u'轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

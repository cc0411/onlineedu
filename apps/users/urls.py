from django.conf.urls import url
from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView,MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView
urlpatterns = [

    url(r'^info/$',UserInfoView.as_view(),name='info'),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image_upload"),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name="update_pwd"),
    # 专用于发送验证码的
    url(r'^sendemail_code/$',
        SendEmailCodeView.as_view(),
        name="sendemail_code"),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name="update_email"),
# 用户中心我的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),

    # 我收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name="myfav_org"),

    # 我收藏的授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 我收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name="myfav_course"),

]

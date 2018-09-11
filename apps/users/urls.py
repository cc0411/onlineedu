from django.conf.urls import url
from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmailCodeView,UpdateEmailView
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


]

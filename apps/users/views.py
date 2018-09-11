from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.core.urlresolvers import reverse
from django.views.generic.base import View
from django.contrib.auth import authenticate,login,logout
from .forms import LoginForm,RegisterForm
from users.models import UserProfile
def index(request):
    return  render(request,'index.html')

class LoginView(View):
    # 直接调用get方法免去判断
    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "login.html", {})
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 取不到时为空，username，password为前端页面name值
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null说明验证成功
            if user is not None:
                # login_in 两参数：request, user
                # 实际是对request写了一部分东西进去，然后在render的时候：
                # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                login(request, user)
                # 跳转到首页 user request会被带回到首页
                return render(request, "index.html")
            # 没有成功说明里面的值是None，并再次跳转回主页面
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误! "})
        else:
            return render(request,'login.html',{'login_form':login_form})

from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{'register_form':register_form})
    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            pass_word = request.POST.get('password','')
            user = UserProfile()
            user.username = user_name
            user.email = user_name
            user.password = make_password(pass_word)
            user.is_active = False
            user.save()
            send_register_email(user_name,"register")
            # 跳转到登录页面
            return render(request, "login.html",{'msg':'邮件已发送，请到邮箱查看'} )
        else:
            return render(request,"register.html",{"register_form":register_form})
from users.models import EmailVerifyRecord
from .forms import ActiveForm

class ActiveUserView(View):
    '''
    用户激活
    '''
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        active_form =ActiveForm(request.GET)
        if all_record:
            for record  in all_record:
                email = record.email
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
                return  render(request,'login.html')
        else:
            return render(request,'register.html',{{"msg": "您的激活链接无效","active_form": active_form}})

from .forms import ForgetForm
class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return  render(request,'forgetpwd.html',{'forget_form':forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email",'')
            send_register_email (email,'forget')
            return  render(request,'login.html',{"msg":"重置密码邮件已发送，请查收"})
        else:
            return render(request,"forgetpwd.html",{"forget_form":forget_form})

class ResetView(View):
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        active_form = ActiveForm(request.GET)
        if all_record:
            for record  in all_record:
                email = record.email
                return render(request,"password_reset.html",{"email":email})
        else:
            return render(request,'forgetpwd.html',{ "msg": "您的重置密码链接无效,请重新请求", "active_form": active_form})

from .forms import ModifyPwdForm
class ModifyPwdView(View):
    def post(self,request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 !=pwd2:
                return  render(request,"password_reset.html",{"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,"login.html",{"msg":"密码修改成功，请重新登录"})
        else:
            email = request.POST.get("email", "")
            return render(
                request, "password_reset.html", {
                    "email": email, "modifypwd_form":modifypwd_form})

#个人信息
from .forms import UserInfoForm,UploadImageForm
from django.http import HttpResponse
import json
class UserInfoView(LoginRequiredMixin,View):
    login_url = 'login'
    redirect_field_name = 'next'
    def get(self,request):
        return render(request,"usercenter-info.html",{})
    def post(self,request):
        user_info_form = UserInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                json.dumps(
                    user_info_form.errors),
                content_type='application/json')


class UploadImageView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                '{"status":"fail"}',
                content_type='application/json')


class UpdatePwdView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            if pwd1 != pwd2:
                return HttpResponse(
                    '{"status":"fail", "msg":"密码不一致"}',
                    content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                json.dumps(
                    modify_form.errors),
                content_type='application/json')

class SendEmailCodeView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request):
        email = request.GET.get("email","")

        if UserProfile.objects.filter(email=email):
            return HttpResponse(
                '{"email":"邮箱已经存在"}',
                content_type='application/json')
        send_register_email(email,"update_email")
        return HttpResponse(
            '{"status":"success"}',
            content_type='application/json')

class UpdateEmailView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def post(self,request):
        email = request.POST.get("email","")
        code = request.POST.get("code","")
        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type="update_email")
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                '{"email":"验证码无效"}',
                content_type='application/json')

class LogoutView(View):
    def get(self, request):
        # django自带的logout
        logout(request)
        # 重定向到首页,
        return redirect(reverse("index"))

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# 实现用户名邮箱均可登录
# 继承ModelBackend类，因为它有方法authenticate，可点进源码查看
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None
from operation.models import UserCourse,UserMessage,UserAsk,Userfav
class MyCourseView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self,request):
        user_courses = UserCourse.objects.filter(user= request.user)
        return render(request,'usercenter-mycourse.html',{"user_courses":user_courses})


from courses.models import CourseOrg,Teacher,Course
class MyFavOrgView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'next'
    def get(self,request):
        org_list = []
        fav_orgs = Userfav.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{"org_list":org_list})

class MyFavTeacherView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'next'
    def get(self,request):
        teacher_list =[]
        fav_teachers = Userfav.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in  fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id =teacher_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{"teacher_list":teacher_list})


class MyFavCourseView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'next'
    def get(self,request):
        course_list = []
        fav_courses = Userfav.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request,'usercenter-fav-course.html',{"course_list":course_list})
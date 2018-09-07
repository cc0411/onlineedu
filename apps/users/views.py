from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from django.contrib.auth import authenticate,login
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
            return render(request, "login.html", )
        else:
            return render(request,"register.html",{"register_form":register_form})
from users.models import EmailVerifyRecord
from .forms import ActiveForm
class ActiveUserView(View):
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

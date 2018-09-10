from django.shortcuts import render
from django.views.generic.base import View
from .models import CourseOrg,CityDict
# Create your views here.
from pure_pagination import  Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse
from operation.models import Userfav
from django.db.models import Q



class OrgView(View):
    def get(self, request):
        #查询所有机构
        all_orgs = CourseOrg.objects.all()
        #热门机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        #所有城市
        all_citys = CityDict.objects.all()
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                address__icontains=search_keywords))
        #按城市过滤
        city_id = request.GET.get("city",'')
        if city_id:
            all_orgs = all_orgs.filter(city_id= int(city_id))
        #按类别过滤
        category = request.GET.get('ct',"")
        if category:
            all_orgs = all_orgs.filter(category=int(category))

        #排序
        sort = request.GET.get('sort',"")
        if sort:
            if sort =="students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")
        #统计过滤后的机构数
        org_nums = all_orgs.count()
        #分页
        try:
            page = request.GET.get('page','1')
        except PageNotAnInteger:
            page = 1
        #每页显示5个
        p = Paginator(all_orgs,5,request=request)
        orgs = p.page(page)


        return render(request, "org-list.html", {"all_orgs":orgs,
                                                 "all_citys":all_citys,
                                                 "org_nums":org_nums,
                                                 'city_id':city_id,
                                                 'category':category,
                                                 'hot_orgs':hot_orgs,
                                                 'sort':sort,
                                                 "search_keywords": search_keywords,})

from .forms import UserAskForm
class UserAskView(View):
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错误,请检查"}', content_type='application/json')

class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):

        current_page = "home"
        #根据id获取机构
        course_org = CourseOrg.objects.get(id= int(org_id))
        #获取机构关联的课程和老师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.course_set.all()[:2]
        has_fav = False
        if request.user.is_authenticated:
            if Userfav.objects.filter(user= request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True
        return render(request,'org-detail-homepage.html',{'all_courses':all_courses,
                                                          'all_teacher':all_teacher,
                                                          'course_org':course_org,
                                                          'has_fav':has_fav,
                                                          'current_page':current_page})

class OrgCourseView(View):
    '''
    机构课程页
    '''
    def get(self,request,org_id):

        current_page = "course"
        #根据id获取机构
        course_org = CourseOrg.objects.get(id = int(org_id))
        #获取机构所有课程
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated:
            if Userfav.objects.filter(user= request.user,fav_id=course_org.id,fav_type=2):
                has_fav= True
        return render(request,'org-detail-course.html',{'all_courses':all_courses,
                                                        'course_org':course_org,
                                                        'has_faf':has_fav,
                                                        'current_page':current_page})

class OrgDescView(View):
    '''
    机构详情页
    '''
    def get(self,request,org_id):

        current_page = "desc"

        course_org = CourseOrg.objects.get(id = int(org_id))

        has_fav = False

        if request.user.is_authenticated:
            if Userfav.objects.filter(user = request.user,fav_id=course_org.id,fav_type =2):
                has_fav = True
        return render(request,'org-detail-desc.html',{'course_org':course_org,
                                                      'current_page':current_page,
                                                      "has_fav":has_fav,
                                                      })

class OrgTeacherView(View):
    def get(self,request,org_id):

        current_page = "teacher"
        course_org = CourseOrg.objects.get(id = int(org_id))

        all_teachers = course_org.teacher_set.all()
        has_fav = False

        if request.user.is_authenticated:
            if Userfav.objects.filter(user = request.user,fav_id = course_org.id,fav_type =2):
                has_fav = True
        return  render(request,'org-detail-teachers.html',{'all_teachers':all_teachers,
                                                           'course_org':course_org,
                                                           'current_page':current_page,
                                                           'has_fav':has_fav})

from courses.models import CourseOrg,Course
from organization.models import Teacher
class AddFavView(View):
    def post(self,request):

        id = request.POST.get('fav_id',0)
        type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg"："未登录"}',content_type='application/json')
        exist_records = Userfav.objects.filter(user=request.user,fav_type=int(type),fav_id=int(id))
        if exist_records:
            #取消收藏相关判断
            exist_records.delete()
            if int(type)==1:
                course = Course.objects.get(id =int(id))
                course.fav_nums -=1
                if course.fav_nums<0:
                    course.fav_nums =0
                course.save()
            elif int(type)==2:
                org = CourseOrg.objects.get(id=int(id))
                org.fav_nums-=1
                if org.fav_nums<0:
                    org.fav_nums =0
                org.save()
            elif int(type)==3:
                teacher = Teacher.objects.get(id=int(id))
                teacher.fav_nums-=1
                if teacher.fav_nums<0:
                    teacher.fav_nums=0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = Userfav()
            if int(type)>0  and int(id)>0:
                user_fav.fav_id = int(id)
                user_fav.fav_type = int(type)
                user_fav.user = request.user
                user_fav.save()
                if int(type) ==1:
                    course = Course.objects.get(id=int(id))
                    course.fav_nums +=1
                    course.save()
                elif int(type)==2:
                    org = CourseOrg.objects.get(id = int(id))
                    org.fav_nums +=1
                    org.save()
                elif int(type)==3:
                    teacher = Teacher.objects.get(id=int(id))
                    teacher.fav_nums+=1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    def get(self,request):
        all_teacher = Teacher.objects.all()
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_teacher = all_teacher.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords))
        rank_teachers = Teacher.objects.all().order_by("-fav_nums")[:5]
        teacher_nums = all_teacher.count()

        sort = request.GET.get("sort","")
        if sort:
            if sort =="hot":
                all_teacher =all_teacher.order_by("-click_nums")

        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page =1
        p = Paginator(all_teacher,4,request=request)

        teachers = p.page(page)

        return render(request,"teachers-list.html",{'all_teachers':teachers,
                                                    "teacher_nums":teacher_nums,
                                                    "sort":sort,
                                                    'rank_teachers':rank_teachers,
                                                    "search_keywords": search_keywords,})


class TeacherDetailView(View):
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id = int(teacher_id))
        all_course = teacher.course_set.all()

        rank_teachers = Teacher.objects.all().order_by("-fav_nums")[:5]

        has_fav_teacher = False
        has_fav_org = False
        if request.user.is_authenticated:
            if Userfav.objects.filter(user=request.user,fav_id=teacher.id,fav_type=3):
                has_fav_teacher = True
            elif Userfav.objects.filter(user= request.user,fav_type=2,fav_id=teacher.id):
                has_fav_org = True
        return render(request,'teacher-detail.html',{'teacher':teacher,
                                                     "all_course":all_course,
                                                     "rank_teachers":rank_teachers,
                                                     "has_fav_org":has_fav_org,
                                                     "has_fav_teacher":has_fav_teacher,
                                                     })










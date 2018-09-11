from django.shortcuts import render
from django.views.generic.base import View
from .models import CourseOrg,Course,CourseResource,Video
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from operation.models import Userfav,CourseComents, UserCourse
from pure_pagination import  Paginator,EmptyPage,PageNotAnInteger
from django.http import  HttpResponse
from django.db.models import Q
class CourseListView(View):
    '''课程列表'''
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")
        # 搜索功能
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # 在name字段进行操作,做like语句的操作。i代表不区分大小写
            # or操作使用Q
            all_course = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))
        sort = request.GET.get('sort', "")
        if sort:
            if sort == "students":
                all_course = all_courses.order_by("-students")
            elif sort == "hot":
                all_course = all_courses.order_by("-click_nums")
        hot_courses = Course.objects.all().order_by("-students")[:3]
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page =1
        p = Paginator(all_courses,4,request=request)
        courses = p.page(page)


        return render(request,'course-list.html',{'all_courses':courses,
                                                  "sort": sort,
                                                  "hot_courses": hot_courses,
                                                  "search_keywords": search_keywords})


class CourseDetailView(View):
    def get(self,request,course_id):

        course = Course.objects.get(id = int(course_id))

        #是否有收藏
        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if Userfav.objects.filter(user= request.user,fav_id=course.id,fav_type=1):
                has_fav_course = True
            if Userfav.objects.filter(user=request.user,fav_type=2,fav_id=course.course_org.id):
                has_fav_org = True
        course.click_nums +=1
        course.save()
        #具有相关标签的课程推荐
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses =[]
        return render(request,"course-detail.html",{'course':course,
                                            'relate_courses':relate_courses,
                                            'has_fav_course':has_fav_course,
                                            'has_fav_org':has_fav_org
        })

class CommentsView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'next'

    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComents.objects.filter(course=course).order_by("-add_time")

        user_courses = UserCourse.objects.filter(course =course)
        user_ids = [user_course.user_id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course_id for user_course in all_user_courses]
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=course.id)[:4]

        return render(request,'course-comment.html',{"course":course,
                                                     "all_resources":all_resources,
                                                     'all_comments':all_comments,
                                                     "relate_courses":relate_courses})

class CourseInfoView(LoginRequiredMixin,View):
    login_url = '/login'
    redirect_field_name = 'next'
    def get(self,request,course_id):
        course = Course.objects.get(id= int(course_id))
        #查询用户是否学习了该课程 ，如果没有则新增
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            course.students+=1
            course.save()
            user_course.save()
        #查询课件
        all_resources = CourseResource.objects.filter(course=course)
        #选出学了这门课程的学生
        user_courses = UserCourse.objects.filter(course =course)
        #取出userid
        user_ids = [user_course.user_id  for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        course_ids = [user_course.course_id  for user_course in all_user_courses]
        #获取学过的其他课程
        relate_courses = Course.objects.filter(id__in = course_ids).order_by("-click_nums").exclude(id=course.id)[:4]
        return render(request,'course-video.html',{'course':course,
                                                   "all_resources":all_resources,
                                                   "relate_courses":relate_courses})


class AddComentsView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments","")
        if int(course_id) >0 and comments:
            course_comments = CourseComents()

            course = Course.objects.get(id= int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')

class VideoPlayView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'next'
    def get(self, request, video_id):
        # 此处的id为表默认为我们添加的值。
        video = Video.objects.get(id=int(video_id))
        # 找到对应的course
        course = video.lesson.course
        # 查询用户是否开始学习了该课，如果还未学习则，加入用户课程表
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 查询课程资源
        all_resources = CourseResource.objects.filter(course=course)
        # 选出学了这门课的学生关系
        user_courses = UserCourse.objects.filter(course=course)
        # 从关系中取出user_id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 这些用户学了的课程,外键会自动有id，取到字段
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [user_course.course_id for user_course in all_user_courses]
        # 获取学过该课程用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums").exclude(id=course.id)[:4]
        # 是否收藏课程
        return render(request, "course-play.html", {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video,
        })
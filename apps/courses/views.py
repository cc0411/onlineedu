from django.shortcuts import render
from django.views.generic.base import View
from .models import CourseOrg,Course,CourseResource
# Create your views here.
from pure_pagination import  Paginator,EmptyPage,PageNotAnInteger

class CourseListView(View):
    '''课程列表'''
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")
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
                                                  "hot_courses": hot_courses})

from operation.models import Userfav
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
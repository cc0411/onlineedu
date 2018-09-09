from django.shortcuts import render
from django.views.generic.base import View
from .models import CourseOrg,CityDict
# Create your views here.
from pure_pagination import  Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse

class OrgView(View):
    def get(self, request):
        #查询所有机构
        all_orgs = CourseOrg.objects.all()
        #热门机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        #所有城市
        all_citys = CityDict.objects.all()
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
                                                 'sort':sort})

from .forms import UserAskForm
class UserAskView(View):
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错误,请检查"}', content_type='application/json')
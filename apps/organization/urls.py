from django.conf.urls import url
from .views import OrgView,UserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView,TeacherListView,TeacherDetailView
urlpatterns = [

    url(r'^list/$',OrgView.as_view(),name='list'),
    url(r'^userask/$',UserAskView.as_view(),name='userask'),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name="org_home"),
    url(r'^course/(?P<org_id>\d+)/$',OrgCourseView.as_view(),name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$',OrgDescView.as_view(),name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$',OrgTeacherView.as_view(),name='org_teacher'),
    url(r'^add_fav/',AddFavView.as_view(),name='add_fav'),
    # 讲师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    # 访问机构讲师
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),



]

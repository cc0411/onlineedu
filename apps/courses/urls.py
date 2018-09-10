from django.conf.urls import url
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddComentsView
urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='list'),
    url('course/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url(r'^comments/(?P<course_id>\d+)/$', CommentsView.as_view(), name="course_comments"),
    url('add_comment/', AddComentsView.as_view(), name="add_comment"),
]

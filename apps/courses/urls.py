from django.conf.urls import url
from .views import CourseListView,CourseDetailView
urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='list'),
    url('course/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),

]

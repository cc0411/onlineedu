from django.conf.urls import url
from .views import OrgView,UserAskView
urlpatterns = [

    url(r'^list/$',OrgView.as_view(),name='list'),
    url(r'^userask/$',UserAskView.as_view(),name='userask'),



]

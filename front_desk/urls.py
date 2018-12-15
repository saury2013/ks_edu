"""ThreeFish URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from front_desk import views

urlpatterns = [
    url(r'^news/(\d+)/$', views.news),
    url(r'^actions/(\d+)/$', views.actions),
    url(r'^news_list/$', views.news_list,name='news_list'),
    url(r'^action_list/$', views.action_list,name='action_list'),
    url(r'^action_list_api/$', views.action_list_api,name='action_list_api'),
    url(r'^news_list_api/$', views.news_list_api,name='news_list_api'),
    url(r'^course_list_api/$', views.course_list_api,name='course_list_api'),
    url(r'^course_list/$', views.course_list,name='course_list'),
    url(r'^material_list/$', views.material_list,name='material_list'),
    url(r'^comment/$', views.comment,name='post_comment'),

]

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
from ks_crm import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^stu_index$', views.stu_index,name='stu_index'),
    url(r'^testing_system', views.testing_system,name='testing_system'),
    url(r'^lesson_video', views.lesson_video,name='lesson_video'),
    url(r'^new_article', views.add_news,name='new_article'),
    url(r'^new_action', views.add_action,name='new_action'),
    url(r'^faq_editors', views.add_FAQ,name='faq_editors'),
    url(r'^new_course', views.add_course,name='new_course'),
    url(r'^profile_editors', views.profile_modify,name='profile_editors'),
    url(r'^image_upload/(\w+)/', views.image_upload),
    url(r'^skin-config.html/', views.skin_config),
    url(r'^test2/', views.test2),

]

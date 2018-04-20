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
from testing_system import views

urlpatterns = [
    url(r'^test_paper/(\d+)/$', views.test_paper),
    url(r'^new_test_paper/$', views.upload_test_paper,name="new_test_paper"),
    url(r'^save_test_paper/$', views.save_test_paper,name="save_test_paper"),
    url(r'^check_answer/$', views.check_answer,name="check_answer"),

]

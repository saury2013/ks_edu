"""ks_edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from ks_edu import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^fd/', include("front_desk.urls")),
    url(r'^crm/', include("ks_crm.urls")),
    url(r'^ts/', include("testing_system.urls")),
    url(r'^$', views.index),
    url(r'^account/login', views.acc_login,name="acc_login"),
    url(r'^account/logout', views.acc_logout,name="acc_logout"),
    url(r'^account/register', views.acc_register,name="acc_register"),
    url(r'^account/password_resetting', views.acc_password_resetting,name="acc_password_resetting"),
]

handler404 = views.page_not_found
handler500 = views.page_error
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

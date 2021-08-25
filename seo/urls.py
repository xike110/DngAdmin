"""seo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url , include#导入了include函数,注意加,号

urlpatterns = [

    url(r'^', include("app.html_urls")),#引入APP项目的首页子配置文件
    # url(r'^mulu/', include("app.html_urls")),
    # url(r'^list', include("app.html_urls")),
    # url(r'^mew', include("app.html_urls")),
    url(r'^dngadmin/', include("app.dngadmin_urls")),  # 引入了对应的应用名称和目录下的URLS子配置文件地址，app/是根目录名称，'app.urls'是app应用目录下urls.py子配置URL文件
]
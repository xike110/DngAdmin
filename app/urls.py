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
from django.conf.urls import url


from . import views

urlpatterns = [   #前端路由映射

	url(r'^$', views.dngadmin),# '^$' 限制根目录   对应地址http://www.域名.com/app/ (分类主目录) 

	#url(r'^app_http/', views.app_http),#对应地址http://www.域名.com/app/django/ (django工具数据库类) 

	#url(r'^app_models/', views.app_models),#对应地址http://www.域名.com/app/django/ (django工具数据库类) 
	url(r'^install/$', views.dngadmin_install),#创建管理员安装
	url(r'^install_post/$', views.dngadmin_install_post),#创建管理员POST
	url(r'^longin/', views.dngadmin_longin),#后台登录首页
	url(r'^longin_post/$', views.dngadmin_longin_post),#授权COOKIE页
	url(r'^out/', views.dngadmin_out),#后台退出
	url(r'^tips', views.dngadmin_tips),#提示页面
	url(r'^ip_address', views.dngadmin_ip_address), #内置IP接口
	
	]


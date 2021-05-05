from django.shortcuts import render
from django.conf.urls import url



from . import html_views


urlpatterns = [
  
    url(r'^$', html_views.index),# '^$' 限制根目录 对应地址  http://www.域名.com/
    
    url(r'^mulu/', html_views.mulu),

	url(r'^zimulu/', html_views.zimulu),#'^zimulu/'限制包含APP地址+zimulu的目录，对应地址http://www.域名.com/app/zimulu/ (目录)

	url(r'^list', html_views.list),#'^list/'限制包含APP地址+newlist的目录，  对应地址 http://www.域名.com/app/list +任意路径  (列表地址)

	url(r'^new', html_views.new),#'^new'通配包含new的地址，APP地址+new后面写什么狗可以访问 对应地址  http://www.域名.com/app/new +任意路径    (内容页地址)



]



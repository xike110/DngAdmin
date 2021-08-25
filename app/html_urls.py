from django.shortcuts import render
from django.conf.urls import url
from . import html_views
# from . import html_login
# from . import html_userdata #用户资料
# from . import html_userpsd #密码修改
# from . import html_nonedemo #空白页面
# from . import html_shenbao   #故障申报
# ⊙1映射替换1⊙







urlpatterns = [

    url(r'^$', html_views.index),# '^$' 限制根目录 对应地址  http://www.域名.com/
    url(r'^mulu/', html_views.mulu),
	url(r'^zimulu/', html_views.zimulu),#'^zimulu/'限制包含APP地址+zimulu的目录，对应地址http://www.域名.com/app/zimulu/ (目录)
	url(r'^sitemap/', html_views.sitemap),#网站地图
	url(r'^list', html_views.list),#'^list/'限制包含APP地址+newlist的目录，  对应地址 http://www.域名.com/app/list +任意路径  (列表地址)
	url(r'^new', html_views.new),#'^new'通配包含new的地址，APP地址+new后面写什么狗可以访问 对应地址  http://www.域名.com/app/new +任意路径    (内容页地址)
	url(r'^http404/', html_views.http404),  # 404页面
	url(r'^http505/', html_views.http505),  # 505页面
	url(r'^dug/', html_views.dug),  # BUG调试页面
	# url(r'^nonedemo/', html_nonedemo.nonedemo), #空白页面
	# url(r'^nonedemo_post/', html_nonedemo.nonedemo_post), #空白页面接收
	# url(r'^userdata/', html_userdata.userdata),#用户资料
	# url(r'^userdata_post/', html_userdata.userdata_post),#用户资料
	# url(r'^userpsd/', html_userpsd.userpsd),#用户资料
	# url(r'^userpsd_post/', html_userpsd.userpsd_post),#用户资料
	# url(r'^login/', html_login.login),#登录页面
	# url(r'^login_post/', html_login.login_post),#登录页面
	# url(r'^register/', html_login.register),# 注册页面
	# url(r'^register_post/', html_login.register_post),# 注册页面接收
	# url(r'^forgot/', html_login.forgot),# 找回密码
	# url(r'^forgot_post/', html_login.forgot_post),# 找回密码接收
	# url(r'^login_csrf/', html_login.csrf_get),#发送验证码接口
	# url(r'^unlock/', html_login.unlock),# 解锁帐号
	# url(r'^unlock_post/', html_login.unlock_post),# 解锁帐号接收
	# url(r'^signout/', html_login.signout),# 退出账户
	# url(r'^shenbao/', html_shenbao.shenbao),  # 故障申报
	# url(r'^shenbao_post/', html_shenbao.shenbao_post),  # 故障申报的post
	# url(r'^shenbao_api_json/', html_shenbao.shenbao_api_json),  # 故障申报的API查询
	# url(r'^shenbao_api_post/', html_shenbao.shenbao_api_post),  # 故障申报的API接收
	# ⊙2映射替换2⊙


]



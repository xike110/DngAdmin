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
from . import dngadmin_index   #后台首页
from . import dngadmin_datahome  #数据仪表盘首页
from . import dngadmin_install #安装创建账号文件
from . import dngadmin_longin   #后台登录页
from . import dngadmin_tips      #提示警告
from . import dngadmin_ip      #ip查询接口
from . import dngadmin_setup      #系统后台设置
# from . import dngadmin_htmlsetup  #前台设置
from . import dngadmin_security   #后台安全
# from . import dngadmin_protect   #前台安全
from . import dngadmin_userdata   #个人资料
from . import dngadmin_userpsd   #密码修改
from . import dngadmin_crud   #后台一键CRUD
#from . import dngadmin_htmlcrud   #前台一键CRUD
from . import dngadmin_userjournal   #登录日志
from . import dngadmin_adminuser   #后台用户管理
# from . import dngadmin_htmluser   #前台会员管理
from . import dngadmin_admingroup #后台用户组
# from . import dngadmin_htmlgroup   #前台用户组
from . import dngadmin_adminmenu   #后台菜单
#from . import dngadmin_htmlmenu   #前台菜单
from . import dngadmin_adminpower   #后台用户组权限
# from . import dngadmin_htmlpower   #前台用户组权限
from . import dngadmin_shell   #shell命令
from . import dngadmin_sms   #短信设置
from . import dngadmin_imgcode   #图码设置
from . import dngadmin_formdemo   #表单组件演示
from . import dngadmin_formkeydemo   #表单构建
from . import dngadmin_xlsdemo   #基础表格
from . import dngadmin_icodemo   #UI图标
from . import dngadmin_btndemo   #按钮组件
from . import dngadmin_paneldemo   #面板排版
from . import dngadmin_choicedemo   #选项面板
from . import dngadmin_noticedemo   #通知提示
from . import dngadmin_meterdemo   #数据仪表
from . import dngadmin_chartdemo   #数据图表
from . import dngadmin_cssdemo   #CSS动画
from . import dngadmin_bulkdemo   #散装部件
from . import dngadmin_popupdemo   #弹窗提示
from . import dngadmin_pluguser   #插件账户
from . import dngadmin_mail   #邮件设置
from . import dngadmin_none   #空白演示
from . import dngadmin_crudlist   #后台一键列表
from . import dngadmin_crudform   #后台一键表单
from . import dngadmin_crudapi   #后台一键API
from . import dngadmin_crudnone   #后台一键其他
# from . import dngadmin_htmlcrudnone   #前台一键其他
#from . import dngadmin_htmlcrudapi   #前台一键API
# from . import dngadmin_htmlcrudform   #前台一键表单
#from . import dngadmin_htmlcrudlist   #前台一键列表
# ⊙1映射替换1⊙

urlpatterns = [   #路由映射

	url(r'^$', dngadmin_index.index),# '^$' 后台主目录
	url(r'^datahome/', dngadmin_datahome.datahome),  # 数据首页
	url(r'^setup/', dngadmin_setup.setup),  # 后台系统设置
	url(r'^setup_post/', dngadmin_setup.setup_post),  # 后台系统设置post
	# url(r'^htmlsetup/', dngadmin_htmlsetup.htmlsetup),  # 前台设置
	# url(r'^htmlsetup_post/', dngadmin_htmlsetup.htmlsetup_post),  # 前台设置post
	url(r'^security/', dngadmin_security.security),  # 后台安全
	url(r'^security_post/', dngadmin_security.security_post),  # 后台安全post
	# url(r'^protect/', dngadmin_protect.protect),  # 前台安全
	# url(r'^protect_post/', dngadmin_protect.protect_post),  # 前台安全post
	url(r'^userdata/', dngadmin_userdata.userdata),  # 个人资料
	url(r'^userdata_post/', dngadmin_userdata.userdata_post),  # 个人资料post
	url(r'^userpsd/', dngadmin_userpsd.userpsd),  # 密码修改
	url(r'^userpsd_post/', dngadmin_userpsd.userpsd_post),  # 密码修改post
	url(r'^crud/', dngadmin_crud.crud),  # 后台一键crud
	url(r'^crud_post/', dngadmin_crud.crud_post),  # 后台一键crud的post
	# url(r'^htmlcrud/', dngadmin_htmlcrud.crud),  # 前台一键crud
	# url(r'^htmlcrud_post/', dngadmin_htmlcrud.crud_post),  # 前台一键crud的post
	url(r'^crudlist/', dngadmin_crudlist.crudlist),  # 后台一键列表
	url(r'^crudlist_post/', dngadmin_crudlist.crudlist_post),  # 后台一键列表的post
	url(r'^crudform/', dngadmin_crudform.crudform),  # 后台一键表单
	url(r'^crudform_post/', dngadmin_crudform.crudform_post),  # 后台一键表单的post
	url(r'^crudapi/', dngadmin_crudapi.crudapi),  # 后台一键API
	url(r'^crudapi_post/', dngadmin_crudapi.crudapi_post),  # 后台一键API的post
	url(r'^crudnone/', dngadmin_crudnone.crudnone),  # 后台一键其他
	url(r'^crudnone_post/', dngadmin_crudnone.crudnone_post),  # 后台一键其他的post
	# url(r'^htmlcrudnone/', dngadmin_htmlcrudnone.htmlcrudnone),  # 前台一键其他
	# url(r'^htmlcrudnone_post/', dngadmin_htmlcrudnone.htmlcrudnone_post),  # 前台一键其他的post
	# url(r'^htmlcrudapi/', dngadmin_htmlcrudapi.htmlcrudapi),  # 前台一键API
	# url(r'^htmlcrudapi_post/', dngadmin_htmlcrudapi.htmlcrudapi_post),  # 前台一键API的post
	# url(r'^htmlcrudform/', dngadmin_htmlcrudform.htmlcrudform),  # 前台一键表单
	# url(r'^htmlcrudform_post/', dngadmin_htmlcrudform.htmlcrudform_post),  # 前台一键表单的post
	# url(r'^htmlcrudlist/', dngadmin_htmlcrudlist.htmlcrudlist),  # 前台一键列表
	# url(r'^htmlcrudlist_post/', dngadmin_htmlcrudlist.htmlcrudlist_post),  # 前台一键列表的post
	url(r'^userjournal/', dngadmin_userjournal.userjournal),  # 登录日志
	url(r'^userjournal_json/', dngadmin_userjournal.userjournal_json),  # 登录日志json
	url(r'^userjournal_added/', dngadmin_userjournal.userjournal_added), #登录新增
	url(r'^userjournal_delete/', dngadmin_userjournal.userjournal_delete),#登录删除
	url(r'^userjournal_update/', dngadmin_userjournal.userjournal_update),  # 登录更新修改
	url(r'^userjournal_search/', dngadmin_userjournal.userjournal_search), #登录搜索
	url(r'^userjournal_api_json/', dngadmin_userjournal.userjournal_api_json), #登录api查询
	url(r'^adminuser/', dngadmin_adminuser.adminuser),  # 后台用户管理
	url(r'^adminuser_json/', dngadmin_adminuser.adminuser_json),  # 后台用户管理json
	url(r'^adminuser_added/', dngadmin_adminuser.adminuser_added),  # 后台用户管理新增
	url(r'^adminuser_delete/', dngadmin_adminuser.adminuser_delete),  # 后台用户管理删除
	url(r'^adminuser_update/', dngadmin_adminuser.adminuser_update),  # 后台用户管理更新修改
	url(r'^adminuser_search/', dngadmin_adminuser.adminuser_search),  # 后台用户管理搜索
	# url(r'^htmluser/', dngadmin_htmluser.htmluser),  # 前台会员管理
	# url(r'^htmluser_json/', dngadmin_htmluser.htmluser_json),  # 前台会员管理json
	# url(r'^htmluser_added/', dngadmin_htmluser.htmluser_added),  # 前台会员管理新增
	# url(r'^htmluser_delete/', dngadmin_htmluser.htmluser_delete),  # 前台会员管理删除
	# url(r'^htmluser_update/', dngadmin_htmluser.htmluser_update),  # 前台会员管理更新修改
	# url(r'^htmluser_search/', dngadmin_htmluser.htmluser_search),  # 前台会员管理搜索
	url(r'^admingroup/', dngadmin_admingroup.admingroup),  # 后台用户组
	url(r'^admingroup_json/', dngadmin_admingroup.admingroup_json),  # 后台用户组json
	url(r'^admingroup_added/', dngadmin_admingroup.admingroup_added),  # 后台用户组新增
	url(r'^admingroup_delete/', dngadmin_admingroup.admingroup_delete),  # 后台用户组删除
	url(r'^admingroup_update/', dngadmin_admingroup.admingroup_update),  # 后台用户组更新修改
	url(r'^admingroup_search/', dngadmin_admingroup.admingroup_search),  # 后台用户组搜索
    # url(r'^htmlgroup/', dngadmin_htmlgroup.htmlgroup),  # 前台用户组
    # url(r'^htmlgroup_json/', dngadmin_htmlgroup.htmlgroup_json),  # 前台用户组json
    # url(r'^htmlgroup_added/', dngadmin_htmlgroup.htmlgroup_added),  # 前台用户组新增
    # url(r'^htmlgroup_delete/', dngadmin_htmlgroup.htmlgroup_delete),  # 前台用户组删除
    # url(r'^htmlgroup_update/', dngadmin_htmlgroup.htmlgroup_update),  # 前台用户组更新修改
    # url(r'^htmlgroup_search/', dngadmin_htmlgroup.htmlgroup_search),  # 前台用户组搜索
	url(r'^adminpower/', dngadmin_adminpower.adminpower),  # 后台用户组权限
	url(r'^adminpower_json/', dngadmin_adminpower.adminpower_json),  # 后台用户组权限json
	url(r'^adminpower_menu/', dngadmin_adminpower.adminpower_menu),  # 后台用户组权限访问
	url(r'^adminpower_added/', dngadmin_adminpower.adminpower_added),  # 后台用户组权限新增
	url(r'^adminpower_delete/', dngadmin_adminpower.adminpower_delete),  # 后台用户组权限删除
	url(r'^adminpower_update/', dngadmin_adminpower.adminpower_update),  # 后台用户组权限更新修改
	url(r'^adminpower_see/', dngadmin_adminpower.adminpower_see),  # 后台用户组权限开发者
	url(r'^adminpower_post/', dngadmin_adminpower.adminpower_post),  # 后台用户组权限POST
	# url(r'^htmlpower/', dngadmin_htmlpower.htmlpower),  # 前台用户组权限
	# url(r'^htmlpower_json/', dngadmin_htmlpower.htmlpower_json),  # 前台用户组权限json
	# url(r'^htmlpower_menu/', dngadmin_htmlpower.htmlpower_menu),  # 前台用户组权限访问
	# url(r'^htmlpower_added/', dngadmin_htmlpower.htmlpower_added),  # 前台用户组权限新增
	# url(r'^htmlpower_delete/', dngadmin_htmlpower.htmlpower_delete),  # 前台用户组权限删除
	# url(r'^htmlpower_update/', dngadmin_htmlpower.htmlpower_update),  # 前台用户组权限更新修改
	# url(r'^htmlpower_see/', dngadmin_htmlpower.htmlpower_see),  # 前台用户组权限开发者
	# url(r'^htmlpower_post/', dngadmin_htmlpower.htmlpower_post),  # 前台用户组权限POST
	url(r'^adminmenu/', dngadmin_adminmenu.adminmenu),  # 后台菜单
	url(r'^adminmenu_json/', dngadmin_adminmenu.adminmenu_json),  # 后台菜单json
	url(r'^adminmenu_added/', dngadmin_adminmenu.adminmenu_added),  # 后台菜单新增
	url(r'^adminmenu_delete/', dngadmin_adminmenu.adminmenu_delete),  # 后台菜单删除
	url(r'^adminmenu_update/', dngadmin_adminmenu.adminmenu_update),  # 后台菜单更新修改
	url(r'^adminmenu_search/', dngadmin_adminmenu.adminmenu_search),  # 后台菜单搜索
	# url(r'^htmlmenu/', dngadmin_htmlmenu.htmlmenu),  # 前台菜单
	# url(r'^htmlmenu_json/', dngadmin_htmlmenu.htmlmenu_json),  # 前台菜单json
	# url(r'^htmlmenu_added/', dngadmin_htmlmenu.htmlmenu_added),  # 前台菜单新增
	# url(r'^htmlmenu_delete/', dngadmin_htmlmenu.htmlmenu_delete),  # 前台菜单删除
	# url(r'^htmlmenu_update/', dngadmin_htmlmenu.htmlmenu_update),  # 前台菜单更新修改
	# url(r'^htmlmenu_search/', dngadmin_htmlmenu.htmlmenu_search),  # 前台菜单搜索
	url(r'^shell/', dngadmin_shell.shell),  # shell命令
	url(r'^shell_post/', dngadmin_shell.shell_post),  # shell命令的post
	url(r'^mail/', dngadmin_mail.mail),  # 邮件设置
	url(r'^mail_post/', dngadmin_mail.mail_post),  # 短信设置的post
	url(r'^mail_api_json/', dngadmin_mail.mail_api_json),  # 邮件设置的API查询
	url(r'^mail_api_post/', dngadmin_mail.mail_api_post),  # 邮件设置的API查询
	url(r'^sms/', dngadmin_sms.sms),  # 短信设置
	url(r'^sms_post/', dngadmin_sms.sms_post),  # 短信设置的post
	url(r'^imgcode/', dngadmin_imgcode.imgcode),  # 图码设置
	url(r'^imgcode_post/', dngadmin_imgcode.imgcode_post),  # 图码设置的post
	url(r'^formkeydemo/', dngadmin_formkeydemo.formkeydemo),  # 表单构建
	url(r'^formkeydemo_post/', dngadmin_formkeydemo.formkeydemo_post),  # 表单构建的post
	url(r'^xlsdemo/', dngadmin_xlsdemo.xlsdemo),  # 基础表格
	url(r'^xlsdemo_post/', dngadmin_xlsdemo.xlsdemo_post),  # 基础表格的post
	url(r'^icodemo/', dngadmin_icodemo.icodemo),  # UI图标
	url(r'^icodemo_post/', dngadmin_icodemo.icodemo_post),  # UI图标的post
	url(r'^btndemo/', dngadmin_btndemo.btndemo),  # 按钮组件
	url(r'^btndemo_post/', dngadmin_btndemo.btndemo_post),  # 按钮组件的post
	url(r'^paneldemo/', dngadmin_paneldemo.paneldemo),  # 面板排版
	url(r'^paneldemo_post/', dngadmin_paneldemo.paneldemo_post),  # 面板排版的post
	url(r'^choicedemo/', dngadmin_choicedemo.choicedemo),  # 选项面板
	url(r'^choicedemo_post/', dngadmin_choicedemo.choicedemo_post),  # 选项面板的post
	url(r'^noticedemo/', dngadmin_noticedemo.noticedemo),  # 通知提示
	url(r'^noticedemo_post/', dngadmin_noticedemo.noticedemo_post),  # 通知提示的post
	url(r'^meterdemo/', dngadmin_meterdemo.meterdemo),  # 数据仪表
	url(r'^meterdemo_post/', dngadmin_meterdemo.meterdemo_post),  # 数据仪表的post
	url(r'^chartdemo/', dngadmin_chartdemo.chartdemo),  # 数据图表
	url(r'^chartdemo_post/', dngadmin_chartdemo.chartdemo_post),  # 数据图表的post
	url(r'^cssdemo/', dngadmin_cssdemo.cssdemo),  # CSS动画
	url(r'^cssdemo_post/', dngadmin_cssdemo.cssdemo_post),  # CSS动画的post
	url(r'^bulkdemo/', dngadmin_bulkdemo.bulkdemo),  # 散装部件
	url(r'^bulkdemo_post/', dngadmin_bulkdemo.bulkdemo_post),  # 散装部件的post
	url(r'^popupdemo/', dngadmin_popupdemo.popupdemo),  # 弹窗提示
	url(r'^popupdemo_post/', dngadmin_popupdemo.popupdemo_post),  # 弹窗提示的post
	url(r'^pluguser/', dngadmin_pluguser.pluguser),  # 插件账户
	url(r'^pluguser_post/', dngadmin_pluguser.pluguser_post),  # 插件账户的post
	url(r'^formdemo/', dngadmin_formdemo.formdemo),  # 表单组件
	url(r'^formdemo_post/', dngadmin_formdemo.formdemo_post),  # 表单组件的post
	url(r'^formdemo_api_json/', dngadmin_formdemo.formdemo_api_json),  # 表单组件的API查询
	url(r'^formdemo_api_post/', dngadmin_formdemo.formdemo_api_post),  # 表单组件的API接收
	url(r'^none/', dngadmin_none.none),  # 空白演示
	url(r'^none_post/', dngadmin_none.none_post),  # 空白演示的post
	# ⊙2映射替换2⊙
	url(r'^install/$', dngadmin_install.install),#创建管理员安装
	url(r'^install_post/$', dngadmin_install.install_post),#创建管理员POST
	url(r'^longin/', dngadmin_longin.longin),#后台登录首页
	url(r'^longin_post/$', dngadmin_longin.longin_post),#授权COOKIE页
	url(r'^login_csrf/', dngadmin_longin.csrf_get),#后台退出
	url(r'^longin_out/', dngadmin_longin.longin_out),#后台退出
	url(r'^tips', dngadmin_tips.tips),#提示页面
	url(r'^ip/', dngadmin_ip.ip), #内置IP接口,已经作废
	url(r'^ip_json', dngadmin_ip.ip_json), #内置IP接口,已经作废
	url(r'^ip_post', dngadmin_ip.ip_post),  # 内置IP接口,已经作废

	
	]


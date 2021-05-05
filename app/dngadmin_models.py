from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.shortcuts import render
import os
import sys
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块
from . import dngadmin_common #公共函数

def dng_install():#安装创建后台表数据
    models.dngroute.objects.create(uid_int=1, name_str='我的数据', icon_str='fa fa-bar-chart', model_str='cover', sort_int=10)  # 创建菜单
    models.dngroute.objects.create(uid_int=2, name_str='数据仪表', url_str='/dngadmin/datahome', superior_int=1, model_str='form', sort_int=20)
    models.dngroute.objects.create(uid_int=3, name_str='系统管理', icon_str='fa fa-cog', model_str='cover',sort_int=30)
    models.dngroute.objects.create(uid_int=4, name_str='后台设置', url_str='/dngadmin/setup', superior_int=3, model_str='form', sort_int=40)
    models.dngroute.objects.create(uid_int=5, name_str='前台设置', url_str='/dngadmin/htmlsetup', superior_int=3, model_str='form', sort_int=50)
    models.dngroute.objects.create(uid_int=6, name_str='后台安全', url_str='/dngadmin/security', superior_int=3, model_str='form', sort_int=60)
    models.dngroute.objects.create(uid_int=7, name_str='前台安全', url_str='/dngadmin/protect', superior_int=3,model_str='form', sort_int=70)
    models.dngroute.objects.create(uid_int=8, name_str='短信设置', url_str='/dngadmin/sms', superior_int=3, model_str='form', sort_int=80)
    models.dngroute.objects.create(uid_int=9, name_str='图码设置', url_str='/dngadmin/imgcode', superior_int=3, model_str='form', sort_int=90)
    models.dngroute.objects.create(uid_int=10, name_str='邮件设置', url_str='/dngadmin/mail', superior_int=3, model_str='form', sort_int=100)
    models.dngroute.objects.create(uid_int=11, name_str='账号设置', icon_str='fa fa-user', model_str='cover', sort_int=110)
    models.dngroute.objects.create(uid_int=12, name_str='个人资料', url_str='/dngadmin/userdata', superior_int=11, model_str='form', sort_int=120)
    models.dngroute.objects.create(uid_int=13, name_str='密码修改', url_str='/dngadmin/userpsd', superior_int=11, model_str='form', sort_int=130)
    models.dngroute.objects.create(uid_int=14, name_str='登录日志', url_str='/dngadmin/userjournal', superior_int=11, model_str='list', sort_int=140)
    models.dngroute.objects.create(uid_int=15, name_str='用户管理', icon_str='fa fa-group', model_str='cover', sort_int=150)
    models.dngroute.objects.create(uid_int=16, name_str='后台用户', url_str='/dngadmin/adminuser', superior_int=15, model_str='list', sort_int=160)
    models.dngroute.objects.create(uid_int=17, name_str='前台会员', url_str='/dngadmin/htmluser', superior_int=15, model_str='list', sort_int=170)
    models.dngroute.objects.create(uid_int=18, name_str='后台用户组', url_str='/dngadmin/admingroup', superior_int=15, model_str='list', sort_int=180)
    models.dngroute.objects.create(uid_int=19, name_str='前台会员组', url_str='/dngadmin/htmlgroup', superior_int=15, model_str='list', sort_int=190)
    models.dngroute.objects.create(uid_int=20, name_str='后台组权限', url_str='/dngadmin/adminpower', superior_int=15, model_str='form', sort_int=200)
    models.dngroute.objects.create(uid_int=21, name_str='前台组权限', url_str='/dngadmin/htmlpower', superior_int=15, model_str='form', sort_int=210)
    models.dngroute.objects.create(uid_int=22, name_str='菜单管理', icon_str='fa fa-list', model_str='cover', sort_int=220)
    models.dngroute.objects.create(uid_int=23, name_str='后台菜单', url_str='/dngadmin/adminmenu', superior_int=22,model_str='list', sort_int=230)
    models.dngroute.objects.create(uid_int=24, name_str='前台菜单', url_str='/dngadmin/htmlmenu', superior_int=22,model_str='list', sort_int=240)
    models.dngroute.objects.create(uid_int=25, name_str='Shell命令', icon_str='fa fa-terminal',model_str='cover', sort_int=250)
    models.dngroute.objects.create(uid_int=26, name_str='在线命令', url_str='/dngadmin/shell', superior_int=25,model_str='list', sort_int=260)
    models.dngroute.objects.create(uid_int=27, name_str='建表管理', url_str='/dngadmin/datasetup', icon_str='fa fa-database',model_str='url', sort_int=270)
    models.dngroute.objects.create(uid_int=28, name_str='应用商店', url_str='/dngadmin/plugin', icon_str='fa fa-paper-plane-o',model_str='url', sort_int=280)
    #菜单管理 - 后台菜单 -前台菜单
    models.dngusergroup.objects.filter(gid_int=1).update(menu_text='|1||2||3||4||5||6||7||8||9||10||11||12||13||14||15||16||17||18||19||20||21||22||23||24||25||26||27||28|') #加菜单权限
    models.dngusergroup.objects.filter(gid_int=1).update(added_text='|1||2||3||4||5||6||7||8||9||10||11||12||13||14||15||16||17||18||19||20||21||22||23||24||25||26||27||28|')#加增加权限
    models.dngusergroup.objects.filter(gid_int=1).update(delete_text='|1||2||3||4||5||6||7||8||9||10||11||12||13||14||15||16||17||18||19||20||21||22||23||24||25||26||27||28|')#加删除权限
    models.dngusergroup.objects.filter(gid_int=1).update(update_text='|1||2||3||4||5||6||7||8||9||10||11||12||13||14||15||16||17||18||19||20||21||22||23||24||25||26||27||28|')#加修改权限
    models.dngusergroup.objects.filter(gid_int=1).update(see_text='|1||2||3||4||5||6||7||8||9||10||11||12||13||14||15||16||17||18||19||20||21||22||23||24||25||26||27||28|')#加查看权限
    models.dngusergroup.objects.filter(gid_int=2).update(menu_text='|1||11||12||13||14|')
    # models.dngusergroup.objects.filter(gid_int=2).update(added_text='|1||11||12||13||14|')
    # models.dngusergroup.objects.filter(gid_int=2).update(delete_text='|1||11||12||13||14|')
    # models.dngusergroup.objects.filter(gid_int=2).update(update_text='|1||11||12||13||14|')
    # models.dngusergroup.objects.filter(gid_int=2).update(see_text='|1||11||12||13||14|')

def html_install():#安装创建前台表数据
    models.route.objects.create(uid_int=1, name_str='用户中心', icon_str='fa fa-home', url_str='/userhome/index',model_str='cover', sort_int=10)
    models.route.objects.create(uid_int=2, name_str='个人资料', url_str='/userhome/userdata', superior_int=1, model_str='form', sort_int=20)
    models.route.objects.create(uid_int=3, name_str='密码修改', url_str='/userhome/userpsd', superior_int=1, model_str='form', sort_int=30)

    models.usergroup.objects.filter(gid_int=1).update(menu_text='|1||2||3|') #加菜单权限
    models.usergroup.objects.filter(gid_int=1).update(added_text='|1||2||3|')#加增加权限
    models.usergroup.objects.filter(gid_int=1).update(delete_text='|1||2||3|')#加删除权限
    models.usergroup.objects.filter(gid_int=1).update(update_text='|1||2||3|')#加修改权限
    models.usergroup.objects.filter(gid_int=1).update(see_text='|1||2||3|')#加查看权限

    models.usergroup.objects.filter(gid_int=2).update(menu_text='|1||2||3|')  # 加菜单权限
    models.usergroup.objects.filter(gid_int=2).update(added_text='|1||2||3|')  # 加增加权限
    models.usergroup.objects.filter(gid_int=2).update(delete_text='|1||2||3|')  # 加删除权限
    models.usergroup.objects.filter(gid_int=2).update(update_text='|1||2||3|')  # 加修改权限
    models.usergroup.objects.filter(gid_int=2).update(see_text='|1||2||3|')  # 加查看权限
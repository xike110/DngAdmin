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
    #models.dngroute.objects.create(uid_int=5, name_str='前台设置', url_str='/dngadmin/htmlsetup', superior_int=3, model_str='form', sort_int=50)
    models.dngroute.objects.create(uid_int=6, name_str='后台安全', url_str='/dngadmin/security', superior_int=3, model_str='form', sort_int=60)
    # models.dngroute.objects.create(uid_int=7, name_str='前台安全', url_str='/dngadmin/protect', superior_int=3,model_str='form', sort_int=70)
    models.dngroute.objects.create(uid_int=9, name_str='邮件设置', url_str='/dngadmin/mail', superior_int=3, model_str='form', sort_int=100)
    models.dngroute.objects.create(uid_int=10, name_str='短信设置', url_str='/dngadmin/sms', superior_int=3, model_str='form', sort_int=80)
    models.dngroute.objects.create(uid_int=11, name_str='账号设置', icon_str='fa fa-user', model_str='cover', sort_int=110)
    models.dngroute.objects.create(uid_int=12, name_str='个人资料', url_str='/dngadmin/userdata', superior_int=11, model_str='form', sort_int=120)
    models.dngroute.objects.create(uid_int=13, name_str='密码修改', url_str='/dngadmin/userpsd', superior_int=11, model_str='form', sort_int=130)
    models.dngroute.objects.create(uid_int=14, name_str='登录日志', url_str='/dngadmin/userjournal', superior_int=11, model_str='list', sort_int=140)
    models.dngroute.objects.create(uid_int=15, name_str='用户管理', icon_str='fa fa-group', model_str='cover', sort_int=150)
    models.dngroute.objects.create(uid_int=16, name_str='后台用户', url_str='/dngadmin/adminuser', superior_int=15, model_str='list', sort_int=160)
    # models.dngroute.objects.create(uid_int=17, name_str='前台会员', url_str='/dngadmin/htmluser', superior_int=15, model_str='list', sort_int=170)
    models.dngroute.objects.create(uid_int=18, name_str='后台用户组', url_str='/dngadmin/admingroup', superior_int=15, model_str='list', sort_int=180)
    # models.dngroute.objects.create(uid_int=19, name_str='前台会员组', url_str='/dngadmin/htmlgroup', superior_int=15, model_str='list', sort_int=190)
    models.dngroute.objects.create(uid_int=20, name_str='后台组权限', url_str='/dngadmin/adminpower', superior_int=15, model_str='form', sort_int=200)
    # models.dngroute.objects.create(uid_int=21, name_str='前台组权限', url_str='/dngadmin/htmlpower', superior_int=15, model_str='form', sort_int=210)
    models.dngroute.objects.create(uid_int=22, name_str='菜单管理', icon_str='fa fa-list', model_str='cover', sort_int=220)
    models.dngroute.objects.create(uid_int=23, name_str='后台菜单', url_str='/dngadmin/adminmenu', superior_int=22,model_str='list', sort_int=230)
    # models.dngroute.objects.create(uid_int=24, name_str='前台菜单', url_str='/dngadmin/htmlmenu', superior_int=22,model_str='list', sort_int=240)
    models.dngroute.objects.create(uid_int=25, name_str='后端工具', icon_str='fa fa-terminal',model_str='cover', sort_int=250)
    models.dngroute.objects.create(uid_int=28, name_str='后台一键列表', url_str='/dngadmin/crudlist', superior_int=25, icon_str='fa fa-desktop', model_str='form', sort_int=280)
    models.dngroute.objects.create(uid_int=29, name_str='后台一键表单', url_str='/dngadmin/crudform', superior_int=25,icon_str='fa fa-desktop', model_str='form', sort_int=290)
    models.dngroute.objects.create(uid_int=30, name_str='后台一键API', url_str='/dngadmin/crudapi', superior_int=25,icon_str='fa fa-desktop', model_str='form', sort_int=300)
    models.dngroute.objects.create(uid_int=31, name_str='后台一键其他', url_str='/dngadmin/crudnone', superior_int=25,icon_str='fa fa-desktop', model_str='form', sort_int=310)
    # models.dngroute.objects.create(uid_int=34, name_str='前台一键表单', url_str='/dngadmin/htmlcrudform', superior_int=25,icon_str='fa fa-desktop', model_str='form', sort_int=340)
    # models.dngroute.objects.create(uid_int=36, name_str='前台一键其他', url_str='/dngadmin/htmlcrudnone', superior_int=25,icon_str='fa fa-desktop', model_str='form', sort_int=360)
    models.dngroute.objects.create(uid_int=40, name_str='前端工具', icon_str='fa fa-html5', model_str='cover',sort_int=400)
    models.dngroute.objects.create(uid_int=41, name_str='表单组件', url_str='/dngadmin/formdemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=410)
    models.dngroute.objects.create(uid_int=42, name_str='表单构建', url_str='/dngadmin/formkeydemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=420)
    models.dngroute.objects.create(uid_int=43, name_str='基础表格', url_str='/dngadmin/xlsdemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=430)
    models.dngroute.objects.create(uid_int=44, name_str='图标素材', url_str='/dngadmin/icodemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=440)
    models.dngroute.objects.create(uid_int=45, name_str='组件按钮', url_str='/dngadmin/btndemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=450)
    models.dngroute.objects.create(uid_int=46, name_str='排版面板', url_str='/dngadmin/paneldemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=460)
    models.dngroute.objects.create(uid_int=47, name_str='栅格面板', url_str='/dngadmin/choicedemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=470)
    models.dngroute.objects.create(uid_int=48, name_str='通知提示', url_str='/dngadmin/noticedemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=480)
    models.dngroute.objects.create(uid_int=49, name_str='统计仪表', url_str='/dngadmin/meterdemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=490)
    models.dngroute.objects.create(uid_int=50, name_str='数据图表', url_str='/dngadmin/chartdemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=500)
    models.dngroute.objects.create(uid_int=51, name_str='CSS动画', url_str='/dngadmin/cssdemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=510)
    models.dngroute.objects.create(uid_int=52, name_str='散装部件', url_str='/dngadmin/bulkdemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=520)
    models.dngroute.objects.create(uid_int=53, name_str='弹窗提示', url_str='/dngadmin/popupdemo', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=530)
    models.dngroute.objects.create(uid_int=54, name_str='空白演示', url_str='/dngadmin/none', superior_int=40,icon_str='fa fa-desktop', model_str='form', sort_int=540)
    models.dngroute.objects.create(uid_int=60, name_str='插件管理', icon_str='fa fa-paper-plane-o', model_str='cover',sort_int=600)
    models.dngroute.objects.create(uid_int=62, name_str='插件商店', url_str='http://www.dngadmin.com/app.html?uid=', superior_int=60, icon_str='fa fa-paper-plane-o',model_str='url', sort_int=620)

    #菜单管理 - 后台菜单 -前台菜单
    models.dngusergroup.objects.filter(gid_int=1).update(menu_text='|1||2||3||4||6||9||10||11||12||13||14||15||16||18||20||22||23||25||28||29||30||31||40||41||42||43||44||45||46||47||48||49||50||51||52||53||54||60||62|') #加菜单权限
    models.dngusergroup.objects.filter(gid_int=1).update(added_text='|1||2||3||4||6||9||10||11||12||13||14||15||16||18||20||22||23||25||28||29||30||31||40||41||42||43||44||45||46||47||48||49||50||51||52||53||54||60||62|')#加增加权限
    models.dngusergroup.objects.filter(gid_int=1).update(delete_text='|1||2||3||4||6||9||10||11||12||13||14||15||16||18||20||22||23||25||28||29||30||31||40||41||42||43||44||45||46||47||48||49||50||51||52||53||54||60||62|')#加删除权限
    models.dngusergroup.objects.filter(gid_int=1).update(update_text='|1||2||3||4||6||9||10||11||12||13||14||15||16||18||20||22||23||25||28||29||30||31||40||41||42||43||44||45||46||47||48||49||50||51||52||53||54||60||62|')#加修改权限
    models.dngusergroup.objects.filter(gid_int=1).update(see_text='|1||2||3||4||6||9||10||11||12||13||14||15||16||18||20||22||23||25||28||29||30||31||40||41||42||43||44||45||46||47||48||49||50||51||52||53||54||60||62|')#加查看权限
    models.dngusergroup.objects.filter(gid_int=2).update(menu_text='|1||2||11||12||13||14|')
    models.dngusergroup.objects.filter(gid_int=2).update(added_text='|1||2||11||12||13||14|')
    models.dngusergroup.objects.filter(gid_int=2).update(delete_text='|1||2||11||12||13||14|')
    models.dngusergroup.objects.filter(gid_int=2).update(update_text='|1||2||11||12||13||14|')
    # models.dngusergroup.objects.filter(gid_int=2).update(see_text='|1||2||11||12||13||14|')

def html_install():#安装创建前台表数据
    models.route.objects.create(uid_int=1, name_str='会员中心', icon_str='fa fa-home', url_str='/userhome',model_str='cover', sort_int=10, prove_bool=True, seotirle_str='会员中心',keywords_str='会员中心', description_str='会员中心')
    # models.route.objects.create(uid_int=2, name_str='个人资料', url_str='/userdata', superior_int=1,model_str='form', sort_int=20, prove_bool=True, seotirle_str='个人资料',keywords_str='个人资料', description_str='个人资料')
    # models.route.objects.create(uid_int=3, name_str='密码修改', url_str='/userpsd', superior_int=1,model_str='form', sort_int=30, prove_bool=True, seotirle_str='密码修改',keywords_str='密码修改', description_str='密码修改')
    models.route.objects.create(uid_int=50, name_str='网站首页', url_str='/', model_str='none',sort_int=500, prove_bool=False,seotirle_str='DngAdmin后台系统-为极速开发而生！', keywords_str='DngAdmin后台系统', description_str='DngAdmin后台系统1.0-基于python和Django原生开发,为极速开发而生')
    models.route.objects.create(uid_int=51, name_str='资讯目录', url_str='/mulu', model_str='none', sort_int=510, prove_bool=False,seotirle_str='资讯目录页-DngAdmin后台系统', keywords_str='资讯目录',description_str='DngAdmin后台系统-资讯目录，DngAdmin后台系统')
    models.route.objects.create(uid_int=52, name_str='目录资讯', url_str='/muluzixun', model_str='cover', sort_int=520,prove_bool=False, seotirle_str='目录资讯-DngAdmin后台系统', keywords_str='目录资讯',description_str='DngAdmin后台系统-目录资讯')
    models.route.objects.create(uid_int=53, name_str='资讯子目录', url_str='/zimulu',superior_int=52, model_str='none', sort_int=530,prove_bool=False, seotirle_str='资讯子目录页-DngAdmin后台系统', keywords_str='资讯子目录',description_str='DngAdmin后台系统-资讯目录')
    models.route.objects.create(uid_int=54, name_str='资讯列表页', url_str='/list', superior_int=52,model_str='none', sort_int=540,prove_bool=False, seotirle_str='资讯列表页-DngAdmin后台系统', keywords_str='资讯列表页',description_str='DngAdmin后台系统-资讯列表页')
    models.route.objects.create(uid_int=55, name_str='资讯内容页', url_str='/new', superior_int=52,model_str='none', sort_int=550,prove_bool=False, seotirle_str='资讯内容页-DngAdmin后台系统', keywords_str='资讯内容页',description_str='DngAdmin后台系统-资讯内容页')
    models.route.objects.create(uid_int=56, name_str='网站地图', url_str='/sitemap', superior_int=52, model_str='none',sort_int=560,display_bool=False,prove_bool=False, seotirle_str='网站地图-DngAdmin后台系统', keywords_str='网站地图',description_str='DngAdmin后台系统-网站地图')
    # models.route.objects.create(uid_int=100, name_str='售后服务', url_str='/shouhoufuwu', model_str='cover', sort_int=1000, prove_bool=True, seotirle_str='付费采集-DngAdmin后台系统', keywords_str='付费采集',description_str='DngAdmin后台系统-付费采集')
    # models.route.objects.create(uid_int=101, name_str='申报登记', url_str='/shenbao', superior_int=100, model_str='form',sort_int=1010, prove_bool=True, seotirle_str='申报登记-DngAdmin后台系统', keywords_str='申报登记', description_str='DngAdmin后台系统-申报登记')
    # models.route.objects.create(uid_int=103, name_str='空白页面', url_str='/nonedemo', superior_int=100, model_str='none', sort_int=1030, prove_bool=True, seotirle_str='空白页面-DngAdmin后台系统', keywords_str='空白页面', description_str='DngAdmin后台系统-空白页面')


    models.usergroup.objects.filter(gid_int=1).update(menu_text='|1||2||3||100||101||103|') #加菜单权限
    models.usergroup.objects.filter(gid_int=1).update(added_text='|1||2||3||100||101||103|')#加增加权限
    models.usergroup.objects.filter(gid_int=1).update(delete_text='|1||2||3||100||101||103|')#加删除权限
    models.usergroup.objects.filter(gid_int=1).update(update_text='|1||2||3||100||101||103|')#加修改权限
    models.usergroup.objects.filter(gid_int=1).update(see_text='|1||2||3||100||101||103|')#加查看权限

    models.usergroup.objects.filter(gid_int=2).update(menu_text='|1||2||3||100||101||103|')  # 加菜单权限
    models.usergroup.objects.filter(gid_int=2).update(added_text='|1||2||3||100||101||103|')  # 加增加权限
    models.usergroup.objects.filter(gid_int=2).update(delete_text='|1||2||3||100||101||103|')  # 加删除权限
    models.usergroup.objects.filter(gid_int=2).update(update_text='|1||2||3||100||101||103|')  # 加修改权限
    # models.usergroup.objects.filter(gid_int=2).update(see_text='|1||2||3|')  # 加查看权限
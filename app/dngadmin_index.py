

# Create your views here.
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
import re
from django.core.cache import cache#缓存
from django.views.decorators.cache import cache_page
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块
from . import dngadmin_common #公共函数



def index(request):#后台首页

    # ----------------------------------------------------------
    #    日记记录与COOKIE验证与权限 》》》开始
    # ----------------------------------------------------------

    gm = request.GET.get('gm')  # 警告
    cache_get = request.GET.get('cache_get')  # 清空缓存
    tishi = request.GET.get('tishi')  # 提示
    jinggao = request.GET.get('jinggao')  # 警告
    yes = request.GET.get('yes')  # 警告


    if "dnguser_uid" in request.COOKIES:  # 判断cookies有无，跳转
        cookie_user_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
                                                    salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
        cookie_user_name = request.get_signed_cookie(key="dnguser_name", default=None,
                                                     salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
        cookie_user_cookie_echo = request.get_signed_cookie(key="dnguser_cookie_echo", default=None,
                                                            salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
        cookie_user_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
                                                       salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

        cookie_pr = dngadmin_common.dng_yanzheng(cookie_user_uid, cookie_user_name, cookie_user_cookie,
                                                 cookie_user_cookie_echo)
        if cookie_pr:
            dnguser_uid = cookie_pr.uid_int  # 赋值ID
            dnguser_name = cookie_pr.username_str  # 赋值用户名
            dnguser_cookie = cookie_pr.cookie_str  # 赋值COOKIE记录
        else:
            return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('检测到非法登录'))

        if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
            if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
                return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('不允许同时登录账号'))
    else:
        return HttpResponseRedirect('/dngadmin/tips/?jinggao=' + parse.quote('您需要重新登录'))

    # ----------------------------------------------------------
    #    日记记录与COOKIE验证与权限《《《 结束
    # ----------------------------------------------------------

    # ----------------------------------------------------------
    #    获取菜单列表》》》开始
    # ----------------------------------------------------------
    group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int) #获取会员组名称

    if "管理员" in group.gname_str and cache_get:
        cache.clear()

        yes ="全部清空缓存成功！"

    #listindex = models.dngroute.objects.filter(~Q(superior_int=0)).order_by('sort_int')  # 取出排序最靠前的,填写进我的首页链接，和默认链接

    # ----------------------------------------------------------
    #   获取菜单列表《《《 结束
    # ----------------------------------------------------------






    return render(request,"dngadmin/index.html",{
        "title":dngadmin_common.dng_setup().setupname_str,#抬头
        "edition": dngadmin_common.dng_setup().edition_str,#版本号
        "file": dngadmin_common.dng_setup().file_str,  # 备案号
        "tongue": dngadmin_common.dng_setup().statistics_text,#统计
        "tishi": tishi,
        "jinggao": jinggao,
        "yes": yes,
        "name":dnguser_name,
        "group_gname":group.gname_str,#用户组昵称
        "group": group.menu_text,
        "gm":gm,
        "caidan": dngadmin_common.dng_daohang(dnguser_uid, gm), # 登陆后菜单









    })








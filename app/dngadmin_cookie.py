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

def dng_ckurl(request):#

    get_url = request.path
    get_url = get_url.split("/")  # 分割
    get_url = get_url[1] + "/" + get_url[2]
    if "_" in get_url:
        url = get_url.split("_")  # 分割
        get_url = url[0]
    uid = models.dngroute.objects.filter(url_str__contains=get_url).first()
    return (uid.uid_int,get_url)


def dng_cookie(request):#
    if "dnguser_uid" in request.COOKIES:  # 判断cookies有无，跳转
        dnguser_uid = request.get_signed_cookie(key="dnguser_uid", default=None,
                                                salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
        dnguser_name = request.get_signed_cookie(key="dnguser_name", default=None,
                                                 salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
        dnguser_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,
                                                   salt=dngadmin_common.dng_anquan().salt_str, max_age=None)



        if dngadmin_common.dng_anquan().tongshi_bool == False:  # 验证是否同时登录
            if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) == False:
                urlstr = '不允许同时登录账号'

                return (urlstr,'不允许同时登录账号')
    else:
        urlstr ='您需要重新登录'

        return (urlstr,'您需要重新登录')

    urlstr ='成功获取'
    return (urlstr,dnguser_name,dnguser_uid,dnguser_cookie)
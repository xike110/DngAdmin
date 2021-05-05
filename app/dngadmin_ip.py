

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
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块
import base64
from . import dngadmin_common #公共函数


def ip(request):#内置ip接口
    a = [0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    zd_list = dngadmin_common.dng_ziduan("dngred")  # 获取对应表下所有字段值

    list = zip(zd_list[0],zd_list[1],a)

    return render(request, "dngadmin/ip.html", {
        "zd_list": zd_list,
        "list": list,


    })

def ip_json(request):#内置ip接口
    models.dngusergroup.objects.filter(gid_int=2).update(
        menu_text='|1||11||12||13||14|')  # 加菜单权限
    models.dngusergroup.objects.filter(gid_int=2).update(
        added_text='|1||11||12||13||14|')  # 加增加权限
    models.dngusergroup.objects.filter(gid_int=2).update(
        delete_text='|1||11||12||13||14|')  # 加删除权限
    models.dngusergroup.objects.filter(gid_int=2).update(
        update_text='|1||11||12||13||14|')  # 加修改权限
    models.dngusergroup.objects.filter(gid_int=2).update(
        see_text='|1||11||12||13||14|')  # 加查看权限
    return HttpResponse()
def ip_post(request):#内置ip接口

    return HttpResponse()
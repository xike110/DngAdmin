from django.shortcuts import render  # 视图渲染模块
from django.http import HttpResponse  # 请求模块
from . import models  # 数据库操作模块
from django.db.models import Q  # 数据库逻辑模块
from django.db.models import Avg, Max, Min, Sum  # 数据库聚合计算模块
from datetime import datetime, timedelta  # Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect  # 重定向模块
from django.shortcuts import render
import os
import sys
from urllib import parse  # 转码
import re  # 正则模块
import random  # 随机模块
import hashlib  # 加密模块
from django.utils import timezone  # 时间处理模块
import datetime  # 时间
import time  # 日期模块


def dng_setup():  # 后台设置
    setup = models.setup.objects.filter(id=1).first()
    return (setup)


def dng_htmlsetup():  # 前台设置
    htmlsetup = models.htmlsetup.objects.filter(id=1).first()
    return (htmlsetup)


def dng_anquan():  # 后台安全
    anquan = models.security.objects.filter(uid_int=1).first()
    return (anquan)


def dng_protect():  # 前台安全
    protect = models.protect.objects.filter(uid_int=1).first()
    return (protect)


def dng_dnguser(uid):  # 查询后台USER
    user = models.dnguser.objects.filter(uid_int=uid).first()
    return (user)


def html_user(uid):  # 查询前台USER
    user = models.user.objects.filter(uid_int=uid).first()
    return (user)


# def dng_gm(uid): #uid查询管理员验证
#     int(uid)
#     ua = models.dnguser.objects.filter(uid_int=uid).first()
#     return ua.gm_bool
# def html_gm(uid): #uid查询管理员验证
#     int(uid)
#     ua = models.user.objects.filter(uid_int=uid).first()
#     return ua.gm_bool
def dng_gmid(id):  # ID查询管理员验证
    int(id)
    ua = models.dnguser.objects.filter(id=id).first()
    return ua.gm_bool


def html_gmid(id):  # ID查询管理员验证
    int(id)
    ua = models.user.objects.filter(id=id).first()
    return ua.gm_bool


def dng_dngred(uid, title, url, user, ip):  # 获取用户设备，并且记录

    if ('iPhone' in user) or ('iPad' in user):
        ua = "ios"
    elif ('Android' in user):
        ua = "安卓"
    else:
        ua = "电脑"

    rizhi = models.dngred.objects.filter(uid_int=uid).order_by('-id').only('url_str').first()

    if not rizhi:

        dngred = models.dngred.objects.create(uid_int=uid, title_str=title, url_str=url, shebei_str=ua, ip_str=ip)
        return dngred
    elif rizhi.url_str == url:
        '拒绝记录日志'
    elif '_json' in url:
        '拒绝记录日志'
    elif '_post' in url:
        '拒绝记录日志'
    elif '_added' in url:
        '拒绝记录日志'
    elif '_delete' in url:
        '拒绝记录日志'
    elif '_update' in url:
        '拒绝记录日志'
    elif '_search' in url:
        '拒绝记录日志'
    else:

        dngred = models.dngred.objects.create(uid_int=uid, title_str=title, url_str=url, shebei_str=ua, ip_str=ip)
        return dngred


def dng_tongshi(uid, cookie):  # 验证cookie相同与否

    user = models.dnguser.objects.filter(uid_int=uid).first()
    if user.cookie_str == cookie:
        cookie = True
        return cookie
    else:
        cookie = False
        return cookie


def dng_usergroup(gid):  # 查询后台会员组
    group = models.dngusergroup.objects.filter(gid_int=gid).first()
    return group


def html_usergroup(gid):  # 查询后台会员组
    group = models.usergroup.objects.filter(gid_int=gid).first()
    return group


def dng_groupall():  # 查询全部后台会员组
    group = models.dngusergroup.objects.filter()
    return group


def html_groupall():  # 查询全部前台会员组
    group = models.usergroup.objects.filter()
    return group


def dng_route(uid):  # 查询后台菜单
    dngroute = models.dngroute.objects.filter(uid_int=uid).first()
    return dngroute


def dng_1route(uid, model):  # 查询带模型菜单
    dngroute = models.dngroute.objects.filter(uid_int=uid, model_str=model).first()
    return dngroute


def dng_ziduan(name):  # 获得对应表名下得所有字段名称
    if name == "setup":
        dbziduan = models.setup._meta.fields
    if name == "security":
        dbziduan = models.security._meta.fields
    if name == "protect":
        dbziduan = models.protect._meta.fields
    if name == "htmlsetup":
        dbziduan = models.htmlsetup._meta.fields
    if name == "dnguser":
        dbziduan = models.dnguser._meta.fields
    if name == "userpsd":
        dbziduan = models.dnguser._meta.fields
    if name == "dngred":
        dbziduan = models.dngred._meta.fields
    if name == "adminuser":
        dbziduan = models.dnguser._meta.fields
    if name == "htmluser":
        dbziduan = models.user._meta.fields
    if name == "admingroup":
        dbziduan = models.dngusergroup._meta.fields
    if name == "htmlgroup":
        dbziduan = models.usergroup._meta.fields
    if name == "adminpower":
        dbziduan = models.dngusergroup._meta.fields
    if name == "htmlpower":
        dbziduan = models.usergroup._meta.fields
    if name == "adminmenu":
        dbziduan = models.dngroute._meta.fields
    if name == "htmlmenu":
        dbziduan = models.route._meta.fields
    if name == "mail":
        dbziduan = models.mail._meta.fields
    # ⊙1数据库模型替换1⊙

    zd_list = []
    for key in dbziduan:
        key = str(key)
        key = key.split(".")  # 分割
        zd_list.append(key[2])

    name_list = []
    for key in zd_list:

        if name == "setup":
            params = models.setup._meta.get_field(key).verbose_name
        if name == "security":
            params = models.security._meta.get_field(key).verbose_name
        if name == "protect":
            params = models.protect._meta.get_field(key).verbose_name
        if name == "htmlsetup":
            params = models.htmlsetup._meta.get_field(key).verbose_name
        if name == "dnguser":
            params = models.dnguser._meta.get_field(key).verbose_name
        if name == "userpsd":
            params = models.dnguser._meta.get_field(key).verbose_name
        if name == "dngred":
            params = models.dngred._meta.get_field(key).verbose_name
        if name == "adminuser":
            params = models.dnguser._meta.get_field(key).verbose_name
        if name == "htmluser":
            params = models.user._meta.get_field(key).verbose_name
        if name == "admingroup":
            params = models.dngusergroup._meta.get_field(key).verbose_name
        if name == "htmlgroup":
            params = models.usergroup._meta.get_field(key).verbose_name
        if name == "adminpower":
            params = models.dngusergroup._meta.get_field(key).verbose_name
        if name == "htmlpower":
            params = models.usergroup._meta.get_field(key).verbose_name
        if name == "adminmenu":
            params = models.dngroute._meta.get_field(key).verbose_name
        if name == "htmlmenu":
            params = models.route._meta.get_field(key).verbose_name
        if name == "mail":
            params = models.mail._meta.get_field(key).verbose_name
        # ⊙2数据库模型替换2⊙

        name_list.append(params)

    return zd_list, name_list


def v_code():  # 随机函数
    ret = ""
    for i in range(10):
        num = random.randint(0, 9)
        # num = chr(random.randint(48,57))#ASCII表示数字
        letter = chr(random.randint(97, 122))  # 取小写字母
        Letter = chr(random.randint(65, 90))  # 取大写字母
        s = str(random.choice([num, letter, Letter]))
        ret += s
    return ret


def dng_ua(userAgent):  # 判断设备

    # 判断用户手机类型开始,py资料真少，此方法从PHP转换过来
    if ('iPhone' in userAgent) or ('iPad' in userAgent):
        ua = "ios"
    elif ('Android' in userAgent):
        ua = "安卓"
    else:
        ua = "电脑"
    return ua


def dng_ckurl(request):  # 判断URL确定权限目录

    get_url = request.path
    get_url = get_url.split("/")  # 分割
    get_url = get_url[1] + "/" + get_url[2]
    if "_" in get_url:
        url = get_url.split("_")  # 分割
        get_url = url[0]
    uid = models.dngroute.objects.filter(url_str__contains=get_url).first()
    return (uid.uid_int, get_url)


def dng_zsgc(dngroute_uid, text):  # 判断增删改查
    added = False  # 增

    if '|' + str(dngroute_uid) + '|' in text:  # 判断增加权限
        added = True

    return (added)

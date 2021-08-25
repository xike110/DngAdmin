from django.shortcuts import render  # 视图渲染模块
from django.http import HttpResponse  # 请求模块
from . import models  # 数据库操作模块
from django.db.models import Q  # 数据库逻辑模块
from django.db.models import Avg, Max, Min, Sum  # 数据库聚合计算模块
from datetime import datetime, timedelta  # Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect  # 重定向模块
from django.shortcuts import render
from django.core.cache import cache
from collections import defaultdict

import os
import subprocess
import sys
import json
import rsa
import base64
from urllib import parse  # 转码
import re  # 正则模块
import random  # 随机模块
import hashlib  # 加密模块
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone  # 时间处理模块
import datetime  # 时间
import time  # 日期模块
from django.forms.models import model_to_dict
import urllib.request #请求模块
import urllib.parse #post请求所需的模块

def dng_setup():  # 后台设置
    setup = models.setup.objects.filter().order_by('id').first()
    return (setup)


def dng_htmlsetup():  # 前台设置
    htmlsetup = models.htmlsetup.objects.filter().order_by('id').first()
    if not htmlsetup:
        htmlsetup =False
    return (htmlsetup)


def dng_anquan():  # 后台安全
    anquan = models.security.objects.filter().order_by('id').first() #最开始的第一条
    return (anquan)


def dng_protect():  # 前台安全
    protect = models.protect.objects.filter().order_by('id').first()
    return (protect)


def dng_dnguser(uid):  # 查询后台USER
    user = models.dnguser.objects.filter(uid_int=uid).first()
    return (user)
def dng_name(name):  # 用户名查询前台USER
    user = models.dnguser.objects.filter(username_str=name).first()
    return (user)

def html_user(uid):  # ID查询前台USER
    user = models.user.objects.filter(uid_int=uid).first()
    return (user)

def html_name(name):  # 用户名查询前台USER
    user = models.user.objects.filter(username_str=name).first()
    return (user)

def dng_mail(email):  # 用户名查询后台邮箱
    user = models.dnguser.objects.filter(emall_str=email).first()
    return (user)
def dng_phone(phone):  # 用户名查询后台邮箱
    user = models.dnguser.objects.filter(mobile_str=phone).first()
    return (user)
def html_mail(email):  # 用户名查询前台邮箱
    user = models.user.objects.filter(emall_str=email).first()
    return (user)
def html_phone(phone):  # 用户名查询前台邮箱
    user = models.user.objects.filter(mobile_str=phone).first()
    return (user)

def dng_gmid(id):  # ID查询管理员验证
    int(id)
    ua = models.dnguser.objects.filter(id=id).first()
    return ua.gm_bool


def html_gmid(id):  # ID查询管理员验证
    int(id)
    ua = models.user.objects.filter(id=id).first()
    return ua.gm_bool

def shebei(user):  # 判断是不是移动设备
    if ('iPhone' in user) or ('iPad' in user):
        return "苹果"
    elif ('Android' in user):
        return "安卓"
    else:
        return "电脑"

def sms_cha(id):  # 查询短信设置
    sms = models.sms.objects.filter(id=id).first()
    return sms

def mail_cha(id):  # 查询短信设置
    mail = models.mail.objects.filter(id=id).first()
    return mail

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

def html_tongshi(uid, cookie):  # 验证cookie相同与否

    user = models.user.objects.filter(uid_int=uid).first()
    if user.cookie_str == cookie:
        cookie = True
        return cookie
    else:
        cookie = False
        return cookie

def get_hash256(data: str): # 对data加密
    hash256 = hashlib.sha256()
    hash256.update(data.encode('utf-8'))
    return hash256.hexdigest()


def rsa_encrypt(message,qianming): #加密 RSA 同时 签名

    #RSA私钥签名
    #:param message: 明文数据
    #:param qianming: 约定好的暗号，或者用户的ID作为签名
    #:return: 签名后的字符串，“|” 分割
    # 导入密钥
    with open('app/ssh/public.pem', 'r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    with open('app/ssh/private.pem', 'r') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

    length = len(message)



    crypto = rsa.encrypt(message.encode("utf-8"), pubkey)# 公钥加密
    crypto_txt=str(base64.b64encode(crypto),encoding = "utf-8") #转base64编码
    qianming_gy = rsa.sign(qianming.encode(), privkey, 'SHA-1')  # 私钥签名
    qianming_txt = str(base64.b64encode(qianming_gy), encoding="utf-8")#转base64编码
    return crypto_txt+"|"+qianming_txt


def rsa_decrypt(message,qianming): #解密 RSA 同时 验算

    #RSA解密验算
    #:param message: 加密数据
    #:param qianming: 约定好的暗号，或者用户的ID作为签名
    #:return: 签名后的字符串，“|” 分割
    with open('app/ssh/public.pem', 'r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    with open('app/ssh/private.pem', 'r') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

    fenge = message.split("|") #先分割
    yans = base64.b64decode(fenge[1])
    if rsa.verify(qianming.encode(), yans, pubkey):
        sign = base64.b64decode(fenge[0])
        return rsa.decrypt(sign,privkey).decode()
    else:

        return ('签名伪造')


def dng_yanzheng(user_uid, user_name,user_cookie,user_cookie_echo):  # 验证cookie
    if not cache.get(user_cookie_echo):
        anquan=dng_protect()
        anquan_salt_str = anquan.salt_str  # 加密盐
        user_cookie_echo_rsa = rsa_decrypt(user_cookie_echo, "多重反复加密，不懂不要改,不理解加QQ:455873983" + user_name)
        user = models.user.objects.filter().order_by("-id")
        ifuid = None
        for ua in user:
            #遍历出匹配的ID
            ce_jiami = str(ua.username_str) + str(ua.password_str) + str(anquan_salt_str)  # 需要解的MD5
            ce_echo = get_hash256(hashlib.md5(ce_jiami.encode(encoding='UTF-8')).hexdigest())  # sha256+MD5加密token
            if ce_echo == user_cookie_echo_rsa:
                ifuid = ua.uid_int

        user = models.user.objects.filter(uid_int=ifuid).first()
        if not user:
            return False
        if dng_anquan().tongshi_bool == False: #验证同时登录是否开启
            if int(user.uid_int) == int(user_uid) and user.username_str ==user_name and user.cookie_str==user_cookie:

                username_post = user.username_str  # 用户账户
                user_password_str = user.password_str  # 用户密码

                cookie_jiami = str(username_post) + str(user_password_str) + str(anquan_salt_str)  # 需要解的MD5
                cookie_echo = get_hash256(hashlib.md5(cookie_jiami.encode(encoding='UTF-8')).hexdigest())  # sha256+MD5加密token
                if user_cookie_echo_rsa==cookie_echo:
                    cache.set(user_cookie_echo, user, 60 * 24)  # 在缓存中设置
                    return user #返回ID,用户名，COOK记录,验证加密盐
                else:
                    return False
            else:
                return False
        else:
            if int(user.uid_int) == int(user_uid) and user.username_str == user_name:

                username_post = user.username_str  # 用户账户
                user_password_str = user.password_str  # 用户密码
                anquan_salt_str = dng_anquan().salt_str  # 加密盐
                cookie_jiami = str(username_post) + str(user_password_str) + str(anquan_salt_str)  # 需要解的MD5
                cookie_echo = get_hash256(hashlib.md5(cookie_jiami.encode(encoding='UTF-8')).hexdigest()) # sha256+MD5加密token
                if user_cookie_echo_rsa == cookie_echo:
                    cache.set(user_cookie_echo, user, 60 * 24)  # 在缓存中设置
                    return user  # 返回ID,用户名，COOK记录,验证加密盐
                else:
                    return False

            else:
                return False
    else:
        return cache.get(user_cookie_echo)

def api_yanzheng(user_uid, user_name,user_token,user_cookie_echo):  # 验证cookie
    if not cache.get(user_cookie_echo):
        anquan = dng_protect()
        anquan_salt_str = anquan.salt_str  # 加密盐
        user_cookie_echo_rsa = rsa_decrypt(user_cookie_echo, "多重反复加密，不懂不要改,不理解加QQ:455873983" + user_name)
        user = models.user.objects.filter().order_by("-id")
        ifuid = None
        for ua in user:
            # 遍历出匹配的ID
            ce_jiami = str(ua.username_str) + str(ua.password_str) + str(anquan_salt_str)  # 需要解的MD5
            ce_echo = get_hash256(hashlib.md5(ce_jiami.encode(encoding='UTF-8')).hexdigest())  # sha256+MD5加密token
            if ce_echo == user_cookie_echo_rsa:
                ifuid = ua.uid_int

        user = models.user.objects.filter(uid_int=ifuid).first()
        if not user:
            return False
        if int(user.uid_int) == int(user_uid) and user.username_str ==user_name and user.token_str==user_token:

            username_post = user.username_str  # 用户账户
            user_password_str = user.password_str  # 用户密码
            anquan_salt_str = dng_anquan().salt_str  # 加密盐
            cookie_jiami = str(username_post) + str(user_password_str) + str(anquan_salt_str)  # 需要解的MD5
            cookie_echo = get_hash256(hashlib.md5(cookie_jiami.encode(encoding='UTF-8')).hexdigest())  # sha256+MD5加密token
            if user_cookie_echo_rsa==cookie_echo:
                cache.set(user_cookie_echo, user, 60 * 24)  # 在缓存中设置
                return user #返回ID,用户名，COOK记录,验证加密盐
            else:
                return False
        else:
            return False
    else:
        return cache.get(user_cookie_echo)



def dng_usergroup(gid):  # 查询后台会员组
    group = models.dngusergroup.objects.filter(gid_int=gid).first()
    return group


def html_usergroup(gid):  # 查询前台会员组
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

def false_daohang(uid,gm):  # 免权限导航
    # -------------------------------------------------------------------
    #   发送的邮件不要带链接,容易被拦截
    #   @uid  =用户ID
    #   @gm   =URL接收管理员切换
    # -------------------------------------------------------------------

    if not cache.get('false_daohang'):

        red = models.route.objects.filter(display_bool=True,prove_bool=False).order_by('sort_int') #获取全部菜单列表
        red2 = models.route.objects.filter(model_str='cover',display_bool=True,prove_bool=False).exclude(uid_int=1).order_by('sort_int')#获取一级菜单列表


        """
        # "id": str(key.id),
        # "uid_int": str(key.uid_int),  # 菜单id
        # "name_str": str(key.name_str),  # 菜单名称
        #"url_str": str(key.url_str),  # 菜单URL
        #"icon_str": str(key.icon_str),  # 菜单图标
        # "model_str": str(key.model_str),  # 菜单模型
        # "superior_int": str(key.superior_int),  # 上级菜单
        # "sort_int": str(key.sort_int),  # 菜单排序
        # "integral_int": str(key.integral_int),  # 积分阈值
        # "money_int": str(key.money_int),  # 余额阈值
        # "totalmoney_int": str(key.totalmoney_int),  # 充值阈值
        # "totalspend_int": str(key.totalspend_int),  # 消费阈值
        # "spread_int": str(key.spread_int),  # 推广阈值
        # "display_bool": str(key.display_bool),  # 菜单显示
        # "prove_bool": str(key.prove_bool),  # 权限验证
        # "seotirle_str": str(key.seotirle_str),  # SEO标题
        # "keywords_str": str(key.keywords_str),  # SEO关键词
        # "description_str": str(key.description_str),  # SEO描述
        """
        data_0 = [] # 最终整合菜单
        data_1= []# 一级菜单
        data_2 = []# 二级菜单

        list_1=None
        list_2 = None

        # ------------------------遍历出二级列表-------------------------

        for key in red2:
            cover = models.route.objects.filter(superior_int=key.uid_int, display_bool=True,prove_bool=False).exclude(superior_int=1).order_by('sort_int')
            for li_key in cover:
                a_href = """<li><a href=\"""" + li_key.url_str + """\">""" + li_key.name_str + """</a></li>"""

                data_2.append({"caidan": key.name_str, "caidan_url": a_href})

        # ------------------------过滤去重键值-------------------------


        ret = []
        ret_id = []

        for data in data_2:
            if data["caidan"] in ret_id:
                id_idx = ret_id.index(data["caidan"])
                current_dict = ret[id_idx]
                for key in current_dict.keys():
                    if key == "caidan":
                        continue


                    current_dict[key] = "{}".format(current_dict[key])+"{}".format( data[key])

            else:
                ret.append(data)
                ret_id.append(data["caidan"])
                continue
        #print(ret)
        # ------------------------遍历出一级列表-------------------------
        for key in red:



            if key.superior_int==0 and not key.model_str=="cover":
                list_1="<li class=\"active\"><a aria-expanded=\"false\" role=\"button\" href=\""+key.url_str+"\">"+key.name_str+"</a></li>"
                data_1.append(list_1)

            elif key.superior_int==0 and key.model_str=="cover" :
                list_1 = """<li class="dropdown active"><a  aria-expanded="false" role="button" href="" class="dropdown-toggle" data-toggle="dropdown">""" + key.name_str + """</a><ul role="menu" class="dropdown-menu"><-二级菜单替换-></ul></li>"""
                data_1.append(list_1)

        for tt in data_1:
            if '<-二级菜单替换->' in tt:
                for mm in ret:

                    if mm["caidan"] in tt and '<-二级菜单替换->' in tt:

                        data_0.append(tt.replace('<-二级菜单替换->', mm["caidan_url"]))
                        if not '<-二级菜单替换->' in data_0:
                            break
            else:
                data_0.append(tt)



        cache.set('false_daohang', data_0, 180)  #

        return (data_0)  # 返回最终结果

    else:



        return (cache.get('false_daohang')) #  返回最终结果

def true_daohang(uid,gm):  # 有权限导航

    # -------------------------------------------------------------------
    #   发送的邮件不要带链接,容易被拦截
    #   @uid  =用户ID
    #   @gm   =URL接收管理员切换
    # -------------------------------------------------------------------
    group = html_usergroup(gid=html_user(uid).group_int)  # 获取会员组名称
    group.menu_text = group.menu_text.strip("|")  # 去两边
    group.menu_text = group.menu_text.split("||")  # 分割

    if not cache.get('true_daohang'+str(uid)):

        red = models.route.objects.filter(display_bool=True, prove_bool=True).order_by('sort_int')  # 获取全部菜单列表
        red2 = models.route.objects.filter(model_str='cover', display_bool=True,prove_bool=True).exclude(uid_int=1).order_by('sort_int')  # 获取一级菜单列表
        """
        # "id": str(key.id),
        # "uid_int": str(key.uid_int),  # 菜单id
        # "name_str": str(key.name_str),  # 菜单名称
        #"url_str": str(key.url_str),  # 菜单URL
        #"icon_str": str(key.icon_str),  # 菜单图标
        # "model_str": str(key.model_str),  # 菜单模型
        # "superior_int": str(key.superior_int),  # 上级菜单
        # "sort_int": str(key.sort_int),  # 菜单排序
        # "integral_int": str(key.integral_int),  # 积分阈值
        # "money_int": str(key.money_int),  # 余额阈值
        # "totalmoney_int": str(key.totalmoney_int),  # 充值阈值
        # "totalspend_int": str(key.totalspend_int),  # 消费阈值
        # "spread_int": str(key.spread_int),  # 推广阈值
        # "display_bool": str(key.display_bool),  # 菜单显示
        # "prove_bool": str(key.prove_bool),  # 权限验证
        # "seotirle_str": str(key.seotirle_str),  # SEO标题
        # "keywords_str": str(key.keywords_str),  # SEO关键词
        # "description_str": str(key.description_str),  # SEO描述
        """
        data_0 = []  # 最终整合菜单
        data_1 = []  # 一级菜单
        data_2 = []  # 二级菜单

        list_1 = None
        list_2 = None

        # ------------------------遍历出二级列表-------------------------
        for mu_key in group.menu_text:  # 遍历菜单权限
            for key in red2:
                cover = models.route.objects.filter(superior_int=key.uid_int, display_bool=True, prove_bool=True).exclude(
                    superior_int=1).order_by('sort_int')

                for li_key in cover:
                    if int(mu_key)==int(li_key.uid_int):
                        a_href = """<li><a href=\"""" + li_key.url_str + """\">""" + li_key.name_str + """</a></li>"""

                        data_2.append({"caidan": key.name_str, "caidan_url": a_href})

        # ------------------------过滤去重键值-------------------------

        ret = []
        ret_id = []

        for data in data_2:
            if data["caidan"] in ret_id:
                id_idx = ret_id.index(data["caidan"])
                current_dict = ret[id_idx]
                for key in current_dict.keys():
                    if key == "caidan":
                        continue

                    current_dict[key] = "{}".format(current_dict[key]) + "{}".format(data[key])

            else:
                ret.append(data)
                ret_id.append(data["caidan"])
                continue
        # print(ret)
        # ------------------------遍历出一级列表-------------------------

        for key in red:



            if key.superior_int == 0 and not key.model_str == "cover":
                for mu_key in group.menu_text:  # 遍历菜单权限
                    if int(mu_key)==int(key.uid_int):
                        list_1 = "<li class=\"active\"><a aria-expanded=\"false\" role=\"button\" href=\"" + key.url_str + "\">" + key.name_str + "</a></li>"
                        data_1.append(list_1)

            elif key.superior_int == 0 and key.model_str == "cover":
                list_1 = """<li class="dropdown active"><a  aria-expanded="false" role="button" href="" class="dropdown-toggle" data-toggle="dropdown">""" + key.name_str + """</a><ul role="menu" class="dropdown-menu"><-二级菜单替换-></ul></li>"""
                data_1.append(list_1)

        for tt in data_1:
            if '<-二级菜单替换->' in tt:
                for mm in ret:

                    if mm["caidan"] in tt and '<-二级菜单替换->' in tt:

                        data_0.append(tt.replace('<-二级菜单替换->', mm["caidan_url"]))
                        if not '<-二级菜单替换->' in data_0:
                            break
            else:
                data_0.append(tt)

        cache.set('true_daohang'+str(uid), data_0, 10)  #

        return (data_0)  # 返回最终结果

    else:

        return (cache.get('true_daohang'+str(uid)))  # 返回最终结果

def home_daohang(uid,gm):#用户中心菜单
    # -------------------------------------------------------------------
    #   发送的邮件不要带链接,容易被拦截
    #   @uid  =用户ID
    #   @gm   =URL接收管理员切换
    # -------------------------------------------------------------------
    group = html_usergroup(gid=html_user(uid).group_int)  # 获取会员组名称
    group.menu_text = group.menu_text.strip("|")  # 去两边
    group.menu_text = group.menu_text.split("||")  # 分割

    if not cache.get('home_daohang' + str(uid)):

        red = models.route.objects.filter(display_bool=True,superior_int=1, prove_bool=True).order_by('sort_int')  # 获取全部菜单列表
        user = html_user(uid)  # 获取用户信息

        """
        # "id": str(key.id),
        # "uid_int": str(key.uid_int),  # 菜单id
        # "name_str": str(key.name_str),  # 菜单名称
        #"url_str": str(key.url_str),  # 菜单URL
        #"icon_str": str(key.icon_str),  # 菜单图标
        # "model_str": str(key.model_str),  # 菜单模型
        # "superior_int": str(key.superior_int),  # 上级菜单
        # "sort_int": str(key.sort_int),  # 菜单排序
        # "integral_int": str(key.integral_int),  # 积分阈值
        # "money_int": str(key.money_int),  # 余额阈值
        # "totalmoney_int": str(key.totalmoney_int),  # 充值阈值
        # "totalspend_int": str(key.totalspend_int),  # 消费阈值
        # "spread_int": str(key.spread_int),  # 推广阈值
        # "display_bool": str(key.display_bool),  # 菜单显示
        # "prove_bool": str(key.prove_bool),  # 权限验证
        # "seotirle_str": str(key.seotirle_str),  # SEO标题
        # "keywords_str": str(key.keywords_str),  # SEO关键词
        # "description_str": str(key.description_str),  # SEO描述
        """
        data_0 = []  # 最终整合菜单
        data_1 = []  # 一级菜单
        data_2 = []  # 二级菜单

        list_1 = None
        list_2 = None

        data_2.append("<li><a>账号：" + user.username_str + "</a></li>")
        data_2.append("<li><a>等级：" + group.gname_str + "</a></li>")
        # data_2.append("<li><a>积分：" + str(user.integral_int) + "</a></li>")
        # data_2.append("<li><a>余额：" + str(user.money_int) + "</a></li>")
        # ------------------------遍历出二级列表-------------------------
        for mu_key in group.menu_text:  # 遍历菜单权限
            for key in red:
                if int(mu_key) == int(key.uid_int):
                    a_href = """<li><a href=\"""" + key.url_str + """\">""" + key.name_str + """</a></li>"""

                    data_2.append(a_href)

        cache.set('home_daohang' + str(uid), data_2, 10)  #

        return (data_2)  # 返回最终结果

    else:

        return (cache.get('home_daohang' + str(uid)))  # 返回最终结果

def dng_ziduan(name):  # 获得对应表名下得所有字段名称
    global choices, params, default
    dbziduan = False
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
    if name == "formdemo":
        dbziduan = models.formdemo._meta.fields
    if name == "pluguser":
        dbziduan = models.pluguser._meta.fields
    if name == "sms":
        dbziduan = models.sms._meta.fields
    if name == "user":
        dbziduan = models.user._meta.fields
    if name == "shenbao":
        dbziduan = models.shenbao._meta.fields
    # ⊙1数据库模型替换1⊙
    if dbziduan==False:
        return False

    zd_list = []
    for key in dbziduan:
        key = str(key)
        key = key.split(".")  # 分割
        zd_list.append(key[2])

    name_list = []
    choices_list = []
    default_list = []
    for key in zd_list:

        if name == "setup":
            params = models.setup._meta.get_field(key).verbose_name
            choices = models.setup._meta.get_field(key).choices
            default = models.setup._meta.get_field(key).default
        if name == "security":
            params = models.security._meta.get_field(key).verbose_name
            choices = models.security._meta.get_field(key).choices
            default = models.security._meta.get_field(key).default
        if name == "protect":
            params = models.protect._meta.get_field(key).verbose_name
            choices = models.protect._meta.get_field(key).choices
            default = models.protect._meta.get_field(key).default
        if name == "htmlsetup":
            params = models.htmlsetup._meta.get_field(key).verbose_name
            choices = models.htmlsetup._meta.get_field(key).choices
            default = models.htmlsetup._meta.get_field(key).default
        if name == "dnguser":
            params = models.dnguser._meta.get_field(key).verbose_name
            choices = models.dnguser._meta.get_field(key).choices
            default = models.dnguser._meta.get_field(key).default
        if name == "userpsd":
            params = models.dnguser._meta.get_field(key).verbose_name
            choices = models.dnguser._meta.get_field(key).choices
            default = models.dnguser._meta.get_field(key).default
        if name == "dngred":
            params = models.dngred._meta.get_field(key).verbose_name
            choices = models.dngred._meta.get_field(key).choices
            default = models.dngred._meta.get_field(key).default
        if name == "adminuser":
            params = models.dnguser._meta.get_field(key).verbose_name
            choices = models.dnguser._meta.get_field(key).choices
            default = models.dnguser._meta.get_field(key).default
        if name == "htmluser":
            params = models.user._meta.get_field(key).verbose_name
            choices = models.user._meta.get_field(key).choices
            default = models.user._meta.get_field(key).default
        if name == "admingroup":
            params = models.dngusergroup._meta.get_field(key).verbose_name
            choices = models.dngusergroup._meta.get_field(key).choices
            default = models.dngusergroup._meta.get_field(key).default
        if name == "htmlgroup":
            params = models.usergroup._meta.get_field(key).verbose_name
            choices = models.usergroup._meta.get_field(key).choices
            default = models.usergroup._meta.get_field(key).default
        if name == "adminpower":
            params = models.dngusergroup._meta.get_field(key).verbose_name
            choices = models.dngusergroup._meta.get_field(key).choices
            default = models.dngusergroup._meta.get_field(key).default
        if name == "htmlpower":
            params = models.usergroup._meta.get_field(key).verbose_name
            choices = models.usergroup._meta.get_field(key).choices
            default = models.usergroup._meta.get_field(key).default
        if name == "adminmenu":
            params = models.dngroute._meta.get_field(key).verbose_name
            choices = models.dngroute._meta.get_field(key).choices
            default = models.dngroute._meta.get_field(key).default
        if name == "htmlmenu":
            params = models.route._meta.get_field(key).verbose_name
            choices = models.route._meta.get_field(key).choices
            default = models.route._meta.get_field(key).default
        if name == "mail":
            params = models.mail._meta.get_field(key).verbose_name
            choices = models.mail._meta.get_field(key).choices
            default = models.mail._meta.get_field(key).default
        if name == "formdemo":
            params = models.formdemo._meta.get_field(key).verbose_name
            choices = models.formdemo._meta.get_field(key).choices
            default = models.formdemo._meta.get_field(key).default

        if name == "pluguser":
            params = models.pluguser._meta.get_field(key).verbose_name
            choices = models.pluguser._meta.get_field(key).choices
            default = models.pluguser._meta.get_field(key).default

        if name == "sms":
            params = models.sms._meta.get_field(key).verbose_name
            choices = models.sms._meta.get_field(key).choices
            default = models.sms._meta.get_field(key).default

        if name == "user":
            params = models.user._meta.get_field(key).verbose_name
            choices = models.user._meta.get_field(key).choices
            default = models.user._meta.get_field(key).default
        if name == "shenbao":
            params = models.shenbao._meta.get_field(key).verbose_name
            choices = models.shenbao._meta.get_field(key).choices
            default = models.shenbao._meta.get_field(key).default
        # ⊙2数据库模型替换2⊙

        if choices:
            choi = choices

        else:
            choi = ""

        if "django.db.models.fields" in str(default):
            defa = ""
        elif default==False:
            defa = ""
        else:
            defa = default

        name_list.append(params)#备注写入列表
        choices_list.append(choi) #元组写入列表
        default_list.append(defa)#默认值写入列表

    geshu = len(zd_list)
    ints_list = []
    for key in range(0, geshu):  # range创建一个整数的范围列表
        ints_list.append(key)


    return zd_list, name_list, ints_list,choices_list,default_list#组合多维数组

    # [0]字段值
    # [1]字段备注
    # [2]数字排列
    # [3]元组，没有返回空(('下拉选项 01', '下拉选项 01'), ('下拉选项 02', '下拉选项 02'), ('下拉选项 03', '下拉选项 03'))
    # [4]返回默认填写值，没有返回空

def v_code_int(weishu):  # 随机数字
    ret = ""
    for i in range(weishu):
        num = random.randint(0, 9)
        s = str(random.choice([num]))
        ret += s
    return ret


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

def v_code_60():  # 随机函数
    ret = ""
    for i in range(60):
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
        ua = "苹果"
    elif ('Android' in userAgent):
        ua = "安卓"
    else:
        ua = "电脑"
    return ua


def dng_ckurl(request):  # 判断后台URL确定权限目录

    get_url = request.path
    get_url = get_url.split("/")  # 分割
    get_url = get_url[1] + "/" + get_url[2]
    if "_" in get_url:
        url = get_url.split("_")  # 分割
        get_url = url[0]
    uid = models.dngroute.objects.filter(url_str__contains=get_url).first()
    return (uid.uid_int, get_url)

def html_ckurl(request):   # 判断前台URL确定权限目录
    get_url = request.path
    if get_url=="/":
        return models.route.objects.filter(url_str=get_url).first()
    elif "_" in get_url:
        url = get_url.split("_")  # 分割
        get_url = url[0]
        return models.route.objects.filter(url_str__contains=get_url).first()
    else:
        get_url = get_url.rstrip("/")
        return models.route.objects.filter(url_str__contains=get_url).first()




def dng_zsgc(dngroute_uid, text):  # 判断增删改查
    added = False  # 增

    if '|' + str(dngroute_uid) + '|' in text:  # 判断增加权限
        added = True

    return (added)

def html_qx_if(dngroute_uid,menu_text,dnguser_integral_int,dngroute_integral_int,dnguser_money_int,dngroute_money_int,dnguser_totalmoney_int,dngroute_totalmoney_int,dnguser_totalspend_int,dngroute_totalspend_int,dnguser_spread_int,dngroute_spread_int): #前端目录权限判断

    if not '|' + str(dngroute_uid) + '|' in menu_text:  # 判断菜单权限
        return "您没有访问这个栏目的权限"
    elif not dnguser_integral_int >= dngroute_integral_int:
        return """您积分""" + str(dnguser_integral_int) + """,访问需要达到""" + str(dngroute_integral_int) + """积分！"""
    elif not dnguser_money_int >= dngroute_money_int:
        return """您余额""" + str(dnguser_money_int) + """元,访问需要达到""" + str(dngroute_money_int) + """余额！"""
    elif not dnguser_totalmoney_int >= dngroute_totalmoney_int:
        return """您累计充值""" + str(dnguser_totalmoney_int) + """,累计充值达到""" + str(dngroute_totalmoney_int) + """元,允许访问"""
    elif not dnguser_totalspend_int >= dngroute_totalspend_int:
        return """您累计消费""" + str(dnguser_totalspend_int) + """,访问需要累计消费达到""" + str(dngroute_totalspend_int) + """元"""
    elif not dnguser_spread_int >= dngroute_spread_int:
        return """您推广""" + str(dnguser_spread_int) + """人,访问需要推广""" + str(dngroute_spread_int) + """人！"""
    else:
        return False



def cmd(command):
    subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    subp.wait(2)
    if subp.poll() == 0:
        return(subp.communicate()[1])
    else:
        return("失败")

def mail_msg(mail_title,user_mail,mail_lei,yanzhengma):# 发送邮件验证码
    # -------------------------------------------------------------------
    #   发送的邮件不要带链接,容易被拦截
    #   @mail_title  =邮件标题
    #   @user_mail   =目标邮件
    #   @mail_lei    =验证码类型
    #   @yanzhengma  =验证码6位数字随机值
    # -------------------------------------------------------------------

    subject = mail_title  # 邮件标题
    from_email = settings.EMAIL_FROM  # 发件人，在settings.py中已经配置
    to_email = user_mail  # 邮件接收者列表

    message = mail_lei+'：' + yanzhengma # 发送的消息
    # message_login  = '登录验证码：' + yanzhengma
    # message_forgot = '找回验证码：' + yanzhengma
    # message_unlock = '解锁验证码：' + yanzhengma
    # message_zhuce  = '注册验证码：' + yanzhengma

    send_mail(subject, message, from_email, [to_email])
    # 之后发送成功会返回True 否则返回False
    if send_mail:
        return('发送成功')

    else:
        return('发送失败')


def sms_msg(phone,yanzhengma,fenlei): #发送短信验证码
    # -------------------------------------------------------------------
    #   @phone         =发送手机号
    #   @yanzhengma    =发送的验证码
    #   @fenlei        =发送分类｛登录,找回,解锁,注册｝
    # -------------------------------------------------------------------
    sms_cha = models.sms.objects.filter().order_by('id').first()
    sms_api=sms_cha.ali_shudanxuan # 短信渠道接口
    appcode_id=sms_cha.appcode_str  # 阿里appcode

    if sms_api=="阿里市场-国阳网":

        """
        # 阿里市场-国阳网-购买链接(https://market.aliyun.com/products/57126001/cmapi00037415.html)
        """
        host = 'https://gyytz.market.alicloudapi.com'
        path = '/sms/smsSend'
        method = 'POST'
        appcode = appcode_id
        querys = 'mobile='+phone+'&param=**code**:' + yanzhengma + ',**minute**:3&minute**%3A5&smsSignId=2e65b1bb3d054466b82f0c9d125465e2&templateId=908e94ccf08b4476ba6c876d13f084ad'
        headers = {'Authorization': 'APPCODE ' + appcode}  # headers中添加上Token口令
        url = host + path + '?' + querys
        postlook = urllib.request.Request(headers=headers, url=url, method=method)  # 模拟post请求
        hpzt = urllib.request.urlopen(postlook).read()  # 请求打开
        data = json.loads(hpzt)
        if "成功" in data['msg'] :
            return('发送成功')
        else:
            return('发送失败')
    elif sms_api=="阿里市场-聚美智数":

        """
        # 阿里市场-聚美智数-购买链接(https://market.aliyun.com/products/57000002/cmapi00046920.html)
        """
        host = 'https://jmsms.market.alicloudapi.com'
        path = '/sms/send'
        method = 'POST'
        appcode = appcode_id
        querys = 'mobile='+phone+'&templateId=M72CB42894&value=' + yanzhengma + ''
        headers = {'Authorization': 'APPCODE ' + appcode}  # headers中添加上Token口令
        url = host + path + '?' + querys
        postlook = urllib.request.Request(headers=headers, url=url, method=method)  # 模拟post请求
        hpzt = urllib.request.urlopen(postlook).read()  # 请求打开
        data = json.loads(hpzt)
        if "成功" in data['msg'] :
            return ('发送成功')
        else:
            return ('发送失败')
    elif sms_api=="阿里市场-鼎信科技":

        """
        # 阿里市场-鼎信科技-购买链接(https://market.aliyun.com/products/56928004/cmapi023305.html)
        """
        host = 'http://dingxin.market.alicloudapi.com'
        path = '/dx/sendSms'
        method = 'POST'
        appcode = appcode_id
        querys = 'mobile='+phone+'&param=code:' + yanzhengma + '&tpl_id=TP1711063'
        headers = {'Authorization': 'APPCODE ' + appcode}  # headers中添加上Token口令
        url = host + path + '?' + querys
        postlook = urllib.request.Request(headers=headers, url=url, method=method)  # 模拟post请求
        hpzt = urllib.request.urlopen(postlook).read()  # 请求打开
        data = json.loads(hpzt)
        if "00000" in data['return_code'] :
            return ('发送成功')
        else:
            return ('发送失败')

    elif sms_api=="阿里市场-云智信":

        """
        # 阿里市场-云智信-购买链接(https://market.aliyun.com/products/56928004/cmapi027248.html)
        """
        host = 'http://yzxyzm.market.alicloudapi.com'
        path = '/yzx/verifySms'
        method = 'POST'
        appcode = appcode_id
        querys = 'phone='+phone+'&templateId=TP18040314&variable=code:' + yanzhengma + ''
        headers = {'Authorization': 'APPCODE ' + appcode}  # headers中添加上Token口令
        url = host + path + '?' + querys
        postlook = urllib.request.Request(headers=headers, url=url, method=method)  # 模拟post请求
        hpzt = urllib.request.urlopen(postlook).read()  # 请求打开
        data = json.loads(hpzt)
        if "00000" in data['return_code']:
            return ('发送成功')
        else:
            return ('发送失败')

    elif sms_api=="阿里市场-深智科技":

        """
        # 阿里市场-深智科技-购买链接(https://market.aliyun.com/products/57124001/cmapi00037170.html)
        """
        postdata = urllib.parse.urlencode({
            "phone_number":phone,
            "template_id":"TPL_0001",
            "content":"code:" + yanzhengma + ",expire_at:3"
        }).encode("utf-8")
        host = 'https://dfsns.market.alicloudapi.com'
        path = '/data/send_sms'
        method = 'POST'
        appcode = appcode_id
        headers = {'Authorization': 'APPCODE ' + appcode}  # headers中添加上Token口令
        url = host + path
        postlook = urllib.request.Request(headers=headers, url=url, data=postdata, method=method)  # 模拟post请求
        hpzt = urllib.request.urlopen(postlook).read()  # 请求打开
        data = json.loads(hpzt)
        if "OK" in data['status']:
            return ('发送成功')
        else:
            return ('发送失败')



    elif sms_api=="自定义短信模块":
        """
               	# -------------------------------------------------------------------
                #        自定义短信接口-根据需求自行开发
                # -------------------------------------------------------------------
                """

        return ('发送成功')

    else:
        """
       	# -------------------------------------------------------------------
        #        默认的短信接口-根据需求自行开发
        # -------------------------------------------------------------------
        """

        return ('发送成功')

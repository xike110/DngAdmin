

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
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块
from . import dngadmin_common #公共函数



def index(request):#后台首页
    title = '后台首页'#标题
    # ----------------------------------------------------------
    #    日记记录与COOKIE验证与权限 》》》开始
    # ----------------------------------------------------------
    ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
    liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
    get_url = request.META.get('QUERY_STRING')# 获取域名后缀的URL
    mulu_url = request.path_info#获取映射路径

    if "dnguser_uid" in request.COOKIES:  # 判断cookies有无，跳转
        dnguser_uid = request.get_signed_cookie(key="dnguser_uid", default=None,salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
        dnguser_name = request.get_signed_cookie(key="dnguser_name", default=None,salt=dngadmin_common.dng_anquan().salt_str, max_age=None)
        dnguser_cookie = request.get_signed_cookie(key="dnguser_cookie", default=None,salt=dngadmin_common.dng_anquan().salt_str, max_age=None)

        if dngadmin_common.dng_anquan().tongshi_bool == False:# 验证是否同时登录
            if dngadmin_common.dng_tongshi(uid=dnguser_uid, cookie=dnguser_cookie) ==False:
                urlstr = parse.quote('不允许同时登录账号')
                response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
                return response
    else:
        urlstr = parse.quote('您需要重新登录')
        response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
        return response

    dngadmin_common.dng_dngred(uid=dnguser_uid,title=title,url=mulu_url,user=liulanqi,ip=ip)#日记记录函数
    # ----------------------------------------------------------
    #    日记记录与COOKIE验证与权限《《《 结束
    # ----------------------------------------------------------
    # ----------------------------------------------------------
    #    获取菜单列表》》》开始
    # ----------------------------------------------------------
    group = dngadmin_common.dng_usergroup(gid=dngadmin_common.dng_dnguser(dnguser_uid).group_int) #获取会员组名称

    listindex = models.dngroute.objects.filter(~Q(superior_int=0)).order_by('sort_int')  # 取出排序最靠前的,填写进我的首页链接，和默认链接





    group.menu_text = group.menu_text.strip("|")#去两边
    group.menu_text = group.menu_text.split("||")#分割

    caidan1_list = []  # 声明为数组的变量
    caidan2_list = []  # 声明为数组的变量

    for key in group.menu_text:  # 遍历菜单权限


        cai = models.dngroute.objects.filter(uid_int=key,model_str='cover',display_bool=True)
        for caidan1 in cai:

            if caidan1:
                caidan1_list.append(caidan1)

                candan2 = models.dngroute.objects.filter(superior_int=caidan1.uid_int, display_bool=True).order_by('sort_int')
                if candan2:

                    caidan2_list.append(candan2)


    # 单链接菜单渲染到视图
    indexurl_list = []
    for key in group.menu_text:

        cai = models.dngroute.objects.filter(uid_int=key, model_str='url',display_bool=True).order_by('sort_int' )
        if cai:
            for caidan in cai:
                indexurl_list.append(caidan)



    # ----------------------------------------------------------
    #   获取菜单列表《《《 结束
    # ----------------------------------------------------------

    return render(request,"dngadmin/index.html",{
        "title":dngadmin_common.dng_setup().setupname_str,#抬头
        "edition": dngadmin_common.dng_setup().edition_str,#版本号
        "file": dngadmin_common.dng_setup().file_str,  # 备案号
        "tongue": dngadmin_common.dng_setup().statistics_text,#统计
        "name":dnguser_name,
        "group_gname":group.gname_str,#用户组昵称
        "group": group.menu_text,
        "indexurl_list": indexurl_list,
        "listindex":listindex[0],

        "caidan1_list": caidan1_list,
        "caidan2_list": caidan2_list,








    })








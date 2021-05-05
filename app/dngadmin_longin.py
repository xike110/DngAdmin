

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

from . import dngadmin_common #公共函数






def longin(request):#后台登录页
	#----------------------------------------------------------
	#    (一) 定义要判断的变量为假 》》》开始
	#----------------------------------------------------------
	graphic =False #图形验证
	cookie  =False #COOKIE验证
	sms    =False #短信验证
	#----------------------------------------------------------
	#    (二) 获取和查询需求判断的值 》》》开始
	#----------------------------------------------------------
	dngurl = request.GET.get('dngurl')  # GET参数
	jinggao_post = request.GET.get('jinggao')  # GET参数
	anquan = models.security.objects.filter(uid_int=1).first()  # 查询安全后缀
	setup= models.setup.objects.filter(id=1).first()  # 查询系统设置
	#----------------------------------------------------------
	#    (三) 流程判断   》》》开始
	#----------------------------------------------------------
	if not dngurl:
		urlstr = parse.quote('请从安全链接入口登录')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)  # 不是安全入口进去跳转提示
		return response
	elif not anquan:
		response = HttpResponseRedirect('/dngadmin/install/')  # 去创建管理员
		return response
	elif not anquan.entrance_str==dngurl:
		urlstr = parse.quote('您的安全加密链接错误')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)  # 不是安全入口进去跳转提示
		return response
	elif anquan.entrance_str == dngurl:
		#涉及到的判断，cookies有无，图形验开关，短信验证

		if "dnguser_uid" in request.COOKIES:#判断cookies有无，跳转后台首页

			dnguser_uid = request.get_signed_cookie(key="dnguser_name", default=None, salt=anquan.salt_str, max_age=None)

			cookie = dnguser_uid
		else:
			cookie= "cookie没有"
		if anquan.sms_bool == True: #判断手机验证
			sms = "手机验证开启"
		else:
			sms = "短信验证没有"
		if anquan.graphic_bool == True: #判断图形验证
			graphic= "图形验证开启"
		else:

			graphic = "图形验证没有"


		return render(request, "dngadmin/login.html", {

			"title": setup.setupname_str,
			"banben": setup.edition_str,
			"tishikey": "您处于安全加密登录",
			"dngurl": dngurl,
			"jinggao_post": jinggao_post,
			"cookie": cookie,
			"sms": sms,
			"graphic": graphic,
		})
	else:

		urlstr = parse.quote('您无权登录')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)  # 不是安全入口进去跳转提示
		return response



def longin_post(request):#cookie授权页

	#----------------------------------------------------------
	#    逻辑流程图
	#----------------------------------------------------------



	#----------------------------------------------------------
	#    (一) 获取和查询需求判断的值 》》》开始
	#----------------------------------------------------------

	username_post = request.POST.get('username', '')  # POST账号
	password_post = request.POST.get('password', '')  # POST密码
	graphic_post  = request.POST.get('password', '')  # POST图形验证码
	sms_post      = request.POST.get('password', '')  # POST短信验证码
	dngurl_post= request.POST.get('dngurl', '')  # POST
	anquan = models.security.objects.filter(uid_int=1).first()  # 查询安全后缀
	user  = models.dnguser.objects.filter(username_str=username_post).first()
	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	password_md5 = hashlib.md5(password_post.encode(encoding='UTF-8')).hexdigest()  # 密码MD5加密

	#----------------------------------------------------------
	#     (二)  登录安全检查-流程判断 》》》开始
	#----------------------------------------------------------

	if not username_post: #判断用户名是不是假
		urlstr = parse.quote('账号不能为空')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)
		return response
	elif not password_post:#判断用户密码是不是假
		urlstr = parse.quote('密码不能为空')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)
		return response
	elif not user:#判断账号嫩否被查询到
		urlstr = parse.quote('账号不存在，请核对账号')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)
		return response
	elif not dngurl_post:#判断入口
		urlstr = parse.quote('请从安全入口提交登录')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)
		return response
	elif not anquan.entrance_str==dngurl_post:#判断安全入口是否正确
		urlstr = parse.quote('您的安全入口不正确')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)
		return response
	elif user.frozen_bool==False:#判断是否被禁止登录
		urlstr = parse.quote('您的账号被封,请联系管理员')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao='+urlstr)
		return response

	else:

		if anquan.area_str:  # 判断地区是否为空
			# ----------------------------------------------------------
			#     根据IP，查出地区，轮询比对数据地区》》》未完成
			# ----------------------------------------------------------
			list_str = anquan.area_str.split("|")
			for key in list_str:  # 遍历字符串，遍历输出

				if ("天津" in key):

					kkk = "包含地区"

				else:  # 都不成立

					urlstr = parse.quote('您地区不符合登录条件')
					response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
					return response



		if anquan.useragent_str:  # 判断允许的设备
			# ----------------------------------------------------------
			#     轮询比对一下数据库设备信息》》》开始
			# ----------------------------------------------------------
			list_str = anquan.useragent_str.split("|")
			for key in list_str:  # 遍历字符串，遍历输出

				if (key in liulanqi):

					kkk = "包含设备"

				else:  # 都不成立

					urlstr = parse.quote('您的设备不符合登录条件')
					response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
					return response

		if user.vipime_time:  # 判断用户登录时限
			# ----------------------------------------------------------
			#     比对时间》》》开始
			# ----------------------------------------------------------
			dq_time = datetime.datetime.now()  # 获取当前系统时间
			dongjie_shijian = (user.vipime_time - datetime.timedelta(hours=0)).strftime("%Y-%m-%d %H:%M:%S")  # 获取之后0小时
			vip_shijian = datetime.datetime.strptime(dongjie_shijian, '%Y-%m-%d %H:%M:%S')# 格式转化

			if dq_time <= vip_shijian:

				kkk = '账号正常期限内'

			else:
				urlstr = parse.quote('您的会员到期，请联系管理员续费')
				response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
				return response



		if anquan.graphic_bool == True:  # 判断图形验证是否开启
			# ----------------------------------------------------------
			#  预留开发
			# ----------------------------------------------------------
			urlstr = parse.quote('图形验证码不正确')
			response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
			return response

		if anquan.sms_bool == True:  # 判断短信验证是否开启
			# ----------------------------------------------------------
			#  预留开发
			# ----------------------------------------------------------
			urlstr = parse.quote('短信验证码不正确')
			response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
			return response

		if anquan.iptxt_text:  # 判断用户登录IP
			# ----------------------------------------------------------
			#     IP地址轮询对比一下》》》开始
			# ----------------------------------------------------------
			list_str = anquan.iptxt_text.split("|")
			for key in list_str:  # 遍历字符串，遍历输出

				if ( key in ip ):

					urlstr = parse.quote('您的IP被限制登录,联系管理员解封')
					response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
					return response

				else:  # 都不成立

					kkk = "不包含ip，不在限制范围"

		if user.frozentime_str:  # 判断冻结时间
			# ----------------------------------------------------------
			#     3.1 进入冻结》》》开始
			# ----------------------------------------------------------
			dq_time = datetime.datetime.now()  # 获取当前系统时间

			jd_shijian = datetime.datetime.strptime(user.frozentime_str, '%Y-%m-%d %H:%M:%S')

			if dq_time >= jd_shijian:

				kkk = '账号解冻时间结束'

			else:

				urlstr = parse.quote('您多次错误输入密码，暂时被冻结账号一段时间')
				response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)
				return response








		anquanjiance = "恭喜通过安全检测"

	#----------------------------------------------------------
	#     (三)  授权COOKIE流程判断 》》》开始
	#----------------------------------------------------------
	if password_md5==user.password_str:

		# ----------------------------------------------------------
		#     3.1 恭喜密码正确,开始授权COOKIE 》》》开始
		# ----------------------------------------------------------

		cookie_md5 = hashlib.md5(dngadmin_common.v_code().encode(encoding='UTF-8')).hexdigest()  # MD5加密token


		response = HttpResponseRedirect('/dngadmin/')  # 设置跳转后的页面地址

		response.set_signed_cookie(key='dnguser_uid', value=user.uid_int, max_age=anquan.prescription_int,salt=anquan.salt_str)  # 把客户账号ID或者用户ID 写入浏览器cookie

		response.set_signed_cookie(key='dnguser_name', value=user.username_str, max_age=anquan.prescription_int,salt=anquan.salt_str)  # 把客户账号ID或者用户ID 写入浏览器cookie

		response.set_signed_cookie(key='dnguser_cookie', value=cookie_md5,max_age=anquan.prescription_int,salt=anquan.salt_str)  # 把客户的MD5值写入浏览器cookie

		models.dnguser.objects.filter(uid_int=user.uid_int).update(cookie_str=cookie_md5,pwderror_int=0,ip_str=ip,shebei_str=dngadmin_common.dng_ua(liulanqi),frozentime_str='')  # 更新修改数据库,存入cookie,清空错误次数，清空冻结时间

		return response

	else:
		# 记录错误次数
		# 判断错误次数超限制，限制登录
		if user.pwderror_int >= anquan.requests_int: #判断错误次数，进入冻结
			# ----------------------------------------------------------
			#     3.1 写入冻结时间》》》开始
			# ----------------------------------------------------------

			datetime.datetime.now()  # 获取当前系统时间
			dongjie_shijian = (datetime.datetime.now() + datetime.timedelta(hours=anquan.psdreq_int)).strftime("%Y-%m-%d %H:%M:%S")  # 获取之后小时

			models.dnguser.objects.filter(uid_int=user.uid_int).update(frozentime_str=dongjie_shijian)  #给账号写入冻结时间

		if password_md5 != user.password_str: #密码不正确开始计错
			cuowu = user.pwderror_int + 1
			models.dnguser.objects.filter(uid_int=user.uid_int).update(pwderror_int=cuowu)  # 更新修改数据库,存入cookie,清空错误次数，清空冻结时间


		urlstr = parse.quote('您的密码错误，请重新输入')
		response = HttpResponseRedirect('/dngadmin/longin/?dngurl='+dngurl_post+'&jinggao='+urlstr)
		return response



def longin_out(request):#cookie清空页

	urlstr = parse.quote('您成功退出账号')
	response = HttpResponseRedirect('/dngadmin/tips/?yes=' + urlstr)
	response.delete_cookie("dnguser_uid")
	response.delete_cookie("dnguser_name")
	response.delete_cookie("dnguser_cookie")

	return response





# Create your views here.
from django.shortcuts import render #视图渲染模块
from django.http import HttpResponse  #请求模块
from . import models #数据库操作模块
from django.db.models import Q #数据库逻辑模块
from django.db.models import Avg,Max,Min,Sum #数据库聚合计算模块
from datetime import datetime,timedelta #Cookie 模块
from django.http import HttpResponse, HttpResponseRedirect #重定向模块
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
import sys
import rsa
import base64
from django.core.cache import cache#缓存
from django.views.decorators.cache import cache_page
import json
from urllib import parse#转码
import re #正则模块
import random#随机模块
import hashlib# 加密模块
from django.utils import timezone #时间处理模块
import datetime#时间
import time# 日期模块

from . import dngadmin_common #公共函数





@csrf_exempt
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
	tishi = request.GET.get('tishi')  # 提示
	jinggao = request.GET.get('jinggao')  # 警告
	yes = request.GET.get('yes')  # 警告
	dngurl = request.GET.get('dngurl')  # GET参数
	#anquan = models.security.objects.filter().order_by('id').first() #最开始的第一条  # 查询安全后缀
	anquan = dngadmin_common.dng_anquan()  # 最开始的第一条  # 查询安全后缀

	#setup= models.setup.objects.filter().order_by('id').first() # 查询系统设置
	setup=  dngadmin_common.dng_setup()  # 查询系统设置
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
			"tishi": tishi,
			"jinggao": jinggao,
			"yes": yes,
			"title": setup.setupname_str,
			"banben": setup.edition_str,
			"tishikey": "您处于安全加密登录",
			"dngurl": dngurl,
			"jinggao_post": jinggao,
			"cookie": cookie,
			"sms": sms,
			"anquan": anquan,  # 前台安全设置
			"graphic": graphic,


		})
	else:

		urlstr = parse.quote('您无权登录')
		response = HttpResponseRedirect('/dngadmin/tips/?jinggao=' + urlstr)  # 不是安全入口进去跳转提示
		return response


@csrf_exempt
def longin_post(request):#cookie授权页

	#----------------------------------------------------------
	#    逻辑流程图
	#----------------------------------------------------------



	#----------------------------------------------------------
	#    (一) 获取和查询需求判断的值 》》》开始
	#----------------------------------------------------------
	csrf = request.POST.get('csrfmiddlewaretoken', '')  # 获取csrf
	username_post = request.POST.get('username', '')  # POST账号
	password_post = request.POST.get('password', '')  # POST密码
	graphic_post  = request.POST.get('graphic', '')  # POST图形验证码
	Verification = request.POST.get('Verification', '')  # 验证码
	dngurl_post= request.POST.get('dngurl', '')  # POST入口
	api_post = request.POST.get('api', '')  # API授权开关
	api_password_post = request.POST.get('api_password', '')  # API授权密码
	api_invalid_post = request.POST.get('invalid', '')  # API授权天数
	#anquan = models.security.objects.filter().order_by('id').first() #最开始的第一条  # 查询安全后缀
	anquan = dngadmin_common.dng_anquan()  # 最开始的第一条  # 查询安全后缀
	user  = models.dnguser.objects.filter(username_str=username_post).first()
	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	if not ip:
		ip = request.META['REMOTE_ADDR']# 原生获取ip信息
	liulanqi = request.META.get('HTTP_USER_AGENT')  # 获取浏览器信息
	password_md5 = hashlib.md5(password_post.encode(encoding='UTF-8')).hexdigest()  # 密码MD5加密
	yuming_url = request.META.get('HTTP_HOST')  # 当前访问的域名

	#----------------------------------------------------------
	#     (二)  登录安全检查-流程判断 》》》开始
	#----------------------------------------------------------

	if not dngadmin_common.dng_name(username_post):
		if api_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': '账号不存在',
			}
			return HttpResponse(json.dumps(data))
		else:
			return HttpResponseRedirect('/dngadmin/longin/&dngurl=' + dngurl_post + '?jinggao=' + parse.quote('账号不存在'))



	if not password_post:#判断用户密码是不是假
		if api_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': '密码不能为空', 
			}
			return HttpResponse(json.dumps(data))
		else:
			return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('密码不能为空'))


	if not user:#判断账号嫩否被查询到
		if api_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': '账号不存在，请核对账号', 
			}
			return HttpResponse(json.dumps(data))
		else:
			return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('账号不存在，请核对账号'))


	if not dngurl_post:#判断入口
		if api_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': '请从安全入口提交登录', 
			}
			return HttpResponse(json.dumps(data))
		else:
			return HttpResponseRedirect('/dngadmin/longin/?jinggao=' + parse.quote('请从安全入口提交登录'))


	if not api_password_post and api_post:  # 判断API密码
		# 下面开始构造JSON格式
		data = {
			'code': '1',
			'msg': 'Api密码未填写',
		}
		return HttpResponse(json.dumps(data))

	if api_post and api_password_post:#判断API密码

		if not anquan.apipsd_str==api_password_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': 'Api密码错误',
			}
			return HttpResponse(json.dumps(data))

	if not anquan.entrance_str==dngurl_post:#判断安全入口是否正确
		if api_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': '您的安全码不正确', 
			}
			return HttpResponse(json.dumps(data))
		else:
			return HttpResponseRedirect('/dngadmin/tishi/?jinggao=' + parse.quote('您的安全码不正确'))


	if user.frozen_bool==False:#判断是否被禁止登录
		if api_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': '您的账号被禁,请联系管理员',
			}
			return HttpResponse(json.dumps(data))
		else:
			return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('您的账号被禁,请联系管理员'))





	if anquan.area_str:  # 判断地区是否为空
		# ----------------------------------------------------------
		#     根据IP，查出地区，轮询比对数据地区》》》未完成
		# ----------------------------------------------------------
		list_str = anquan.area_str.split("|")
		for key in list_str:  # 遍历字符串，遍历输出

			if ("火星" in key):

				kkk = "包含地区"

			else:  # 都不成立
				if api_post:
					# 下面开始构造JSON格式
					data = {
						'code': '1',
						'msg': '您地区不符合登录条件',
					}
					return HttpResponse(json.dumps(data))
				else:
					return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('您地区不符合登录条件'))





	if anquan.useragent_str:  # 判断允许的设备
		# ----------------------------------------------------------
		#     轮询比对一下数据库设备信息》》》开始
		# ----------------------------------------------------------
		list_str = anquan.useragent_str.split("|")
		for key in list_str:  # 遍历字符串，遍历输出

			if (key in liulanqi):

				kkk = "包含设备"

			else:  # 都不成立
				if api_post:
					# 下面开始构造JSON格式
					data = {
						'code': '1',
						'msg': '您的设备不符合登录条件',
					}
					return HttpResponse(json.dumps(data))
				else:
					return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('您的设备不符合登录条件'))



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
			if api_post:
				# 下面开始构造JSON格式
				data = {
					'code': '1',
					'msg': '您的账户到期，请联系管理员续期',
				}
				return HttpResponse(json.dumps(data))
			else:
				return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('您的账户到期，请联系管理员续期'))





	if anquan.station_bool == True and not api_post or anquan.sms_bool == True and not api_post:  # 判断图形验证是否开启
		if not cache.get(csrf):
			return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('验证码失效'))
		elif  not Verification:
			return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('验证码不能为空'))
		elif Verification ==cache.get(csrf):
			ok="验证码正确"
		else:

			return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('验证码错误!'))



	if anquan.iptxt_text:  # 判断用户登录IP
		# ----------------------------------------------------------
		#     IP地址轮询对比一下》》》开始
		# ----------------------------------------------------------
		list_str = anquan.iptxt_text.split("|")
		for key in list_str:  # 遍历字符串，遍历输出
			key = key.replace('.*', '')  # 过滤
			if ( key in ip ):
				if api_post:
					# 下面开始构造JSON格式
					data = {
						'code': '1',
						'msg': '您的IP被限制登录,联系管理员解封',
					}
					return HttpResponse(json.dumps(data))
				else:
					return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('您的IP被限制登录,联系管理员解封'))



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
			if api_post:
				# 下面开始构造JSON格式
				data = {
					'code': '1',
					'msg': '您多次错误输入密码，暂时被冻结账号一段时间',
				}
				return HttpResponse(json.dumps(data))
			else:
				return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('您多次错误输入密码，暂时被冻结账号一段时间'))


	"""
	# ----------------------------------------------------------
	#     恭喜通过安全检测--下面开始授权
	# ----------------------------------------------------------
	"""


	if password_md5==user.password_str:

		# ----------------------------------------------------------
		#     3.1 恭喜密码正确,开始授权COOKIE 》》》开始
		# ----------------------------------------------------------

		dq_time = datetime.datetime.now()  # 获取当前系统时间
		username_post = user.username_str  # 用户账户
		user_password_str = user.password_str  # 用户密码
		anquan_salt_str = anquan.salt_str  # 加密盐
		cookie_jiami = str(username_post) + str(user_password_str) + str(anquan_salt_str) #需要解的MD5
		cookie_jiami_arry = str(dq_time) + str(username_post) + str(user_password_str) + str(anquan_salt_str)+str(dngadmin_common.v_code_60())#不需要解的MD5

		cookie_echo = dngadmin_common.rsa_encrypt(dngadmin_common.get_hash256(hashlib.md5(cookie_jiami.encode(encoding='UTF-8')).hexdigest()),"多重反复加密，不懂不要改,不理解加QQ:455873983"+user.username_str)  # sha256+MD5加密token
		cookie_md5 = dngadmin_common.get_hash256(dngadmin_common.rsa_encrypt(dngadmin_common.get_hash256(hashlib.md5(cookie_jiami_arry.encode(encoding='UTF-8')).hexdigest()),"多重反复加密，不懂不要改,不理解加QQ:455873983"+user.username_str))   # sha256+MD5加密token
		token_echo = dngadmin_common.get_hash256(dngadmin_common.rsa_encrypt(dngadmin_common.get_hash256(hashlib.md5(cookie_jiami_arry.encode(encoding='UTF-8')).hexdigest()),"多重反复加密，不懂不要改,不理解加QQ:455873983"+user.username_str))   # sha256+MD5加密token

		if api_post:
			#判断是不是API授权
			if api_invalid_post:
				api_invalid_post =int(api_invalid_post)*86400
			else:
				api_invalid_post =86400
			# 下面开始构造JSON格式
			cookie_data = {
				'uid': user.uid_int,  # 客户账号ID
				'username': user.username_str,  # 客户账户
				'cookie': cookie_echo,  # cookie口令
				'token': token_echo,  # token口令
			}
			json_data= {
				'code': '0',
				'msg': '成功',
				'data': cookie_data,
			}
			# 返回成功格式
			# {
			# 	"code": "200",
			# 	"message": "成功",
			# 	"data": {
			# 		"uid_int": 1,
			# 		"username_str": "admin",
			# 		"cookie_echo": "ca6f8e0e759ff334b23cfc8f767631ef88884534294b94814a8115136a2bc2f26",
			# 		"token_echo": "026e247489125eb21ce97151a5004a63823422be45cb67452c9415724a1c98f3"
			# 	}
			# }

			response = HttpResponse(json.dumps(json_data))  # 设置跳转后的页面地址

			response.set_signed_cookie(key='dnguser_uid', value=user.uid_int, max_age=api_invalid_post,salt=anquan.salt_str)  # 把客户账号ID或者用户ID 写入浏览器cookie

			response.set_signed_cookie(key='dnguser_name', value=user.username_str, max_age=api_invalid_post,salt=anquan.salt_str)  # 把客户账号名或者用户ID 写入浏览器cookie

			response.set_signed_cookie(key='dnguser_cookie_echo', value=cookie_echo,max_age=api_invalid_post,salt=anquan.salt_str)  # 把客户cookie值写入浏览器cookie

			response.set_signed_cookie(key='dnguser_token_echo', value=token_echo, max_age=api_invalid_post,salt=anquan.salt_str)  # 把客户的cookie值写入浏览器cookie

			models.dnguser.objects.filter(uid_int=user.uid_int).update(token_str=token_echo,pwderror_int=0,ip_str=ip,shebei_str=dngadmin_common.dng_ua(liulanqi),frozentime_str='')  # 更新修改数据库,存入cookie,清空错误次数，清空冻结时间

			return response


		else:
			response = HttpResponseRedirect('/dngadmin/')  # 设置跳转后的页面地址

			response.set_signed_cookie(key='dnguser_uid', value=user.uid_int, max_age=anquan.prescription_int,
									   salt=anquan.salt_str)  # 把客户账号ID或者用户ID 写入浏览器cookie

			response.set_signed_cookie(key='dnguser_name', value=user.username_str, max_age=anquan.prescription_int,
									   salt=anquan.salt_str)  # 把客户账号ID或者用户ID 写入浏览器cookie

			response.set_signed_cookie(key='dnguser_cookie_echo', value=cookie_echo, max_age=anquan.prescription_int,
									   salt=anquan.salt_str)  # 把客户的MD5值写入浏览器cookie

			response.set_signed_cookie(key='dnguser_cookie', value=cookie_md5, max_age=anquan.prescription_int,
									   salt=anquan.salt_str)  # 把客户的MD5值写入浏览器cookie

			models.dnguser.objects.filter(uid_int=user.uid_int).update(cookie_str=cookie_md5, pwderror_int=0, ip_str=ip,
																	   shebei_str=dngadmin_common.dng_ua(liulanqi),
																	   frozentime_str='')  # 更新修改数据库,存入cookie,清空错误次数，清空冻结时间

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

		if api_post:
			# 下面开始构造JSON格式
			data = {
				'code': '1',
				'msg': '密码错误', 
			}
			return HttpResponse(json.dumps(data))
		else:
			return HttpResponseRedirect('/dngadmin/longin/?dngurl=' + dngurl_post + '&jinggao=' + parse.quote('密码错误'))



def csrf_get(request): # 发送验证码接口
	setup = dngadmin_common.dng_setup()  # 获取前台配置


	# -------------------------------------------------------------------
	#                  获取请求
	# -------------------------------------------------------------------

	ip = request.META.get('HTTP_X_FORWARDED_FOR')  # 获取ip信息
	if not ip:
		ip = request.META['REMOTE_ADDR']# 原生获取ip信息
	riqi = time.strftime("%Y-%m-%d", time.localtime())
	login = request.POST.get('login', '')  # 提交登录
	# forgot = request.POST.get('forgot', '')  # 提交找回密码
	# unlock = request.POST.get('unlock', '')  # 提交解锁账户
	# register = request.POST.get('register', '')  # 提交注册帐号


	user = request.POST.get('user', '')  # 获取用户名
	phone = request.POST.get('phone', '')  # 获取手机号
	email = request.POST.get('email', '')  # 获取邮箱
	password = request.POST.get('password', '')  # 获取密码
	passwords = request.POST.get('passwords', '')  # 获取重复密码

	mail_csrf = request.POST.get('mail_csrf', '')  # 获取邮件csrf
	phone_csrf = request.POST.get('phone_csrf', '')  # 获取手机csrf


	# -------------------------------------------------------------------
	#        限制IP每天请求验证码次数，防恶意消耗验验证资源
	# -------------------------------------------------------------------


	stop86400 = True
	# day_mail_ci = False  # 邮箱每日次数
	# day_mail_shi = False  # 邮箱验证码时效
	# day_phone_ci = False  # 短信每日次数
	# day_phone_shi = False  # 短信验证码时效
	if dngadmin_common.mail_cha(1):
		mail_cha =dngadmin_common.mail_cha(1)
		day_mail_ci = mail_cha.requests_int# 邮箱每日次数
		day_mail_shi = mail_cha.youxiao_int# 邮箱验证码时效
	else:
		day_mail_ci = 30 # 邮箱每日次数
		day_mail_shi = 180  # 邮箱验证码时效

	if dngadmin_common.sms_cha(1):
		sms_cha = dngadmin_common.sms_cha(1)
		day_phone_ci = sms_cha.requests_int # 短信每日次数
		day_phone_shi = sms_cha.youxiao_int # 短信验证码时效
	else:
		day_phone_ci = 20 # 短信每日次数
		day_phone_shi = 180  # 短信验证码时效



	# if not day_mail_ci and not day_mail_shi:
	# 	day_mail_ci = 50  # 邮箱每日次数
	# 	day_mail_shi = 180  # 邮箱验证码时效
	#
	# if not day_phone_ci and not day_phone_shi:
	# 	day_phone_ci = 30  # 短信每日次数
	# 	day_phone_shi = 180  # 短信验证码时效


	if mail_csrf:
		cache.get_or_set(riqi + ip + "mail", 0, 86400)
		cache_ip_mail = cache.incr(riqi + ip + "mail")
		if int(cache_ip_mail) >= day_mail_ci:  # 这里控制一个IP24小时申请多少次
			stop86400 = False
	elif phone_csrf:
		cache.get_or_set(riqi + ip + "phone", 0, 86400)
		cache_ip_phone = cache.incr(riqi + ip + "phone")
		if int(cache_ip_phone) >= day_phone_ci:
			stop86400 = False


	# -------------------------------------------------------------------
	#        限制60秒内请求验证码
	# -------------------------------------------------------------------

	stop60 = True

	if not cache.add(ip,0,60):# 这里60，限制60秒内请求验证码
		if mail_csrf:
			cache.decr(riqi + ip + "mail")
		elif phone_csrf:
			cache.decr(riqi + ip + "phone")
		stop60 = False

	# -------------------------------------------------------------------
	#                   判断业务属性,处理发送验证码
	#	@发送成功,返回"True"
	#
	#	@验证码已经发送失败,返回"False"
	#
	#	@账户不存在,返回"None"
	#
	#	@停止发送，原因发送间隔不够60秒,返回"stop60"
	#
	#	@请求验证码次数过多，24小时后再试 返回"stop86400"
	#
	#	@提供信息不正确！验证失败, 返回空
	# -------------------------------------------------------------------

	echo = None

	if login and stop86400 and stop60:
		password=hashlib.md5(password.encode(encoding='UTF-8')).hexdigest()
		# -------------------------------------------------------------------
		#                   登录-验证码发送
		# -------------------------------------------------------------------
		if phone_csrf and user and password:# 判断手机-发送验证码
			# --------判断手机-发送验证码--------------


			user_db = dngadmin_common.dng_name(user)  # 查询用户

			if user_db and user_db.username_str:

				if password==user_db.password_str:# 核对密码
					# --------获取各方参数，执行发送验证码函数--------------
					yanzhengma = dngadmin_common.v_code_int(6)  # 随机6位数字
					send_sms = dngadmin_common.sms_msg(user_db.mobile_str,yanzhengma,"登录")  # 发送验证码函数
					if send_sms == '发送成功':
						# --------验证码写入缓存--------------
						cache.get_or_set(phone_csrf, yanzhengma, day_phone_shi)  # 验证码写入缓存，有效期180秒
						echo = True
					elif send_sms == '发送失败':
						cache.delete(ip)  # 删除60秒限制
						echo = False

				else:
					cache.delete(ip)  # 删除60秒限制
					echo = 'psd_no'  # 密码错误

			else:
				cache.delete(ip)  # 删除60秒限制
				echo = None  # 用户不存在

		elif mail_csrf and user  and password:# 判断邮箱-发送验证码
			# --------判断邮箱-发送验证码--------------

			user_db= dngadmin_common.dng_name(user)  # 查询用户

			if user_db and user_db.username_str:
				if password == user_db.password_str:  # 核对密码
					# --------获取各方参数，执行发送验证码函数--------------
					yanzhengma = dngadmin_common.v_code_int(6)#随机6位数字
					send_mail =dngadmin_common.mail_msg(setup.setupname_str+"-登录",user_db.emall_str,"登录验证码",yanzhengma) #发送验证码函数
					if send_mail=='发送成功':
						# --------验证码写入缓存--------------
						cache.get_or_set(mail_csrf, yanzhengma, 180)#验证码写入缓存，有效期180秒
						echo = True
					elif send_mail=='发送失败':
						cache.delete(ip)  # 删除60秒限制
						echo = False
				else:
					cache.delete(ip)  # 删除60秒限制
					echo = 'psd_no'  # 密码错误
			else:
				cache.delete(ip)  # 删除60秒限制
				echo = None #用户不存在
		else:
			cache.delete(ip)  # 删除60秒限制
			echo = ''

	elif stop60==False:
		# -------------------------------------------------------------------
		#                   返回60秒限制
		# -------------------------------------------------------------------
		echo = 'stop60'

	elif stop86400==False:
		# -------------------------------------------------------------------
		#                   禁止24小时内再请求验证码
		# -------------------------------------------------------------------
		cache.delete(ip)  # 删除60秒限制
		echo = 'stop86400'

	return HttpResponse(echo)


def longin_out(request):#cookie清空页

	urlstr = parse.quote('您成功退出账号')
	response = HttpResponseRedirect('/dngadmin/tips/?yes=' + urlstr)
	response.delete_cookie("dnguser_uid")
	response.delete_cookie("dnguser_name")
	response.delete_cookie("dnguser_cookie")
	response.delete_cookie("dnguser_cookie_echo")

	return response


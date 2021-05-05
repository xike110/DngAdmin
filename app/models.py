from django.db import models
import random#随机模块
# str后缀 == models.CharField_字符串
# text后缀 == models.TextField_富文本编辑
# int后缀 == models.IntegerField整形数字
# float后缀 == models.FloatField浮点小数点类型
# bool后缀 == models.BooleanField_布尔真假类型
# time == models.DateTimeField_日期+时间
#注意事项：(一) 不要用自增id，来作为用户ID或者业务id，不少新手都会这种方法，会使得业务与id生成强耦合，导致id生成算法难以升级，未来分布式数据库，和分表都会麻烦
#注意事项：(二) 不要修改已经建立的数据库字段，会带来未知风险，建议对字段新增，不要删除修改系统已经存在的数据库字段，
#注意事项：(三) 创建字段名称记得带类型后缀，方便前台识别，生成对应表单输入样式
#注意事项：(四) 你不确定未来会迁移什么类型数据库，为了保证通用，尽量全部小写，慎用驼峰命名法，数据库高手忽略此条
class user(models.Model):#前台会员表

	uid_int           = models.IntegerField(blank=False, verbose_name='会员ID')#会员ID, 设置不能为空
	username_str      = models.CharField(max_length=255, unique=True, blank=False, verbose_name='会员账号') #会员账号, unique不能重复，不许为空
	password_str      = models.CharField(max_length=255, blank=False, verbose_name='会员密码') #会员密码MD5加密，不许为空
	name_str          = models.CharField(max_length=255, blank=True, verbose_name='昵称') #会员昵称
	gender_str        = models.CharField(max_length=255, blank=True, verbose_name='性别') #性别，默认空
	introduce_str     = models.CharField(max_length=255, blank=True, verbose_name='个人简介') #个人简介，默认空
	emall_str         = models.CharField(max_length=255, blank=True, verbose_name='邮箱') #会员邮箱
	mobile_str        = models.CharField(max_length=255, blank=True, verbose_name='手机号') #手机号接收短信等
	group_int         = models.IntegerField(default=2, verbose_name='用户组')#填写用户组ID
	rank_str          = models.CharField(max_length=255, blank=True, verbose_name='等级')
	gm_bool           = models.BooleanField(default=False, verbose_name='前台管理')  # 账号超级管理员开关，False=不是超级管理 True=是超级管理员
	money_int         = models.IntegerField(default=0, verbose_name='余额')#余额，默认值为0，不支持小数点
	totalmoney_int    = models.IntegerField(default=0, verbose_name='累计充值')  # 默认值为0，不支持小数点
	totalspend_int    = models.IntegerField(default=0, verbose_name='累计消费')  # 默认值为0，不支持小数点
	integral_int      = models.IntegerField(default=0, verbose_name='积分')#积分，默认值为0
	spread_int        = models.IntegerField(default=0, verbose_name='推广注册')  # 默认值为0，不支持小数点
	ip_str            = models.CharField(max_length=255, blank=True, verbose_name='登录IP') #登录ip地址
	shebei_str        = models.CharField(max_length=255, blank=True, verbose_name='登录设备') #登录后台设备
	cookie_str 		  = models.CharField(max_length=255, blank=True, verbose_name='cookie')  # 后台客户cookie
	token_str         = models.CharField(max_length=255, blank=True, verbose_name='token密钥') #后台客户token密钥，预留加密授权登录用
	days_int          = models.IntegerField(default=0, verbose_name='登录天数')#登录天数
	pwderror_int      = models.IntegerField(default=0, verbose_name='密错次数')#密码错误次数
	frozen_bool       = models.BooleanField(default=False, verbose_name='禁止登录') #账号限制登录，False=没有禁止 True=账号禁止
	frozentime_str    = models.CharField(max_length=255, blank=True, verbose_name='冻结时间') #冻结
	vipime_time       = models.DateTimeField(blank=True, default='2099-12-28 23:59:59', verbose_name='登录时限')   # 登录有效期，开通一年有效期，半年有效期会员账号用
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间') #后台注册时间
	update_time       = models.DateTimeField(auto_now=True, verbose_name='更新时间')#最后一次登录时间



class dnguser(models.Model):#后台会员表

	uid_int           = models.IntegerField(blank=False, verbose_name='会员ID')#会员ID, 设置不能为空
	username_str      = models.CharField(max_length=255, unique=True, blank=False, verbose_name='会员账号') #会员账号, unique不能重复，不许为空
	password_str      = models.CharField(max_length=255, blank=False, verbose_name='会员密码') #会员密码MD5加密，不许为空
	name_str          = models.CharField(max_length=255, blank=True, verbose_name='昵称') #会员昵称
	gender_str        = models.CharField(max_length=255, blank=True, verbose_name='性别') #性别，默认空
	introduce_str     = models.CharField(max_length=255, blank=True, verbose_name='个人简介') #个人简介，默认空
	emall_str         = models.CharField(max_length=255, blank=True, verbose_name='邮箱') #会员邮箱
	mobile_str        = models.CharField(max_length=255, blank=True, verbose_name='手机号') #手机号接收短信等
	group_int         = models.IntegerField(default=2, verbose_name='用户组')#填写用户组ID
	rank_str          = models.CharField(max_length=255, blank=True, verbose_name='等级')
	gm_bool           = models.BooleanField(default=False, verbose_name='超级管理')  # 账号超级管理员开关，False=不是超级管理 True=是超级管理员
	money_int         = models.IntegerField(default=0, verbose_name='余额')#余额，默认值为0，不支持小数点
	totalmoney_int    = models.IntegerField(default=0, verbose_name='累计充值')  # 默认值为0，不支持小数点
	totalspend_int    = models.IntegerField(default=0, verbose_name='累计消费')  # 默认值为0，不支持小数点
	integral_int      = models.IntegerField(default=0, verbose_name='积分')#积分，默认值为0
	spread_int        = models.IntegerField(default=0, verbose_name='推广注册')#默认值为0，不支持小数点
	ip_str            = models.CharField(max_length=255, blank=True, verbose_name='登录IP') #登录ip地址
	shebei_str        = models.CharField(max_length=255, blank=True, verbose_name='登录设备') #登录后台设备
	cookie_str 		  = models.CharField(max_length=255, blank=True, verbose_name='cookie')  # 后台客户cookie
	token_str         = models.CharField(max_length=255, blank=True, verbose_name='token密钥') #后台客户token密钥，预留加密授权登录用
	days_int          = models.IntegerField(default=0, verbose_name='登录天数')#登录天数
	pwderror_int      = models.IntegerField(default=0, verbose_name='密错次数')#密码错误次数
	frozen_bool       = models.BooleanField(default=True, verbose_name='允许登录') #账号限制登录，False=没有禁止 True=账号禁止
	frozentime_str    = models.CharField(max_length=255, blank=True, verbose_name='冻结时间') #冻结
	vipime_time       = models.DateTimeField(blank=True, default='2099-12-28 23:59:59', verbose_name='登录时限')   # 登录有效期，开通一年有效期，半年有效期会员账号用
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间') #后台注册时间
	update_time       = models.DateTimeField(auto_now=True, verbose_name='更新时间')#最后一次登录时间


class usergroup(models.Model): #前台会员组表
	gid_int           = models.IntegerField(blank=False, unique=True, verbose_name='用户组id')
	gname_str         = models.CharField(max_length=255, unique=True, blank=False, verbose_name='用户组名称')
	uperior_int       = models.IntegerField(default=0, verbose_name='上级用户组') #0没有上级，填写菜单ID
	integral_int      = models.IntegerField(default=0, verbose_name='积分阈值')
	money_int         = models.IntegerField(default=0, verbose_name='余额阈值')
	totalmoney_int    = models.IntegerField(default=0, verbose_name='充值阈值')
	totalspend_int    = models.IntegerField(default=0, verbose_name='消费阈值')
	spread_int        = models.IntegerField(default=0, verbose_name='推广阈值')
	added_int         = models.IntegerField(default=0, verbose_name='每日新增')
	look_int          = models.IntegerField(default=0, verbose_name='每日查看')
	space_int         = models.IntegerField(default=0, verbose_name='每日上传')
	download_int      = models.IntegerField(default=0, verbose_name='每日下载')
	trial_bool        = models.BooleanField(default=False, verbose_name='自动过审')
	upload_bool       = models.BooleanField(default=False, verbose_name='上传权限')
	download_bool     = models.BooleanField(default=False, verbose_name='下载权限')
	menu_text         = models.TextField(blank=True, verbose_name='菜单权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	added_text        = models.TextField(blank=True, verbose_name='新增权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	delete_text       = models.TextField(blank=True, verbose_name='删除权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	update_text       = models.TextField(blank=True, verbose_name='修改权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	see_text          = models.TextField(blank=True, verbose_name='查看权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|，PS:拥有菜单权限，就默认可以查看菜单，此查看权限是，方便设置此菜单下一些查看带星号手机之类的权限

class dngusergroup(models.Model):  #后台用户组表
	gid_int           = models.IntegerField(blank=False, unique=True, verbose_name='用户组id')
	gname_str         = models.CharField(max_length=255, unique=True, blank=False, verbose_name='用户组名称')
	uperior_int       = models.IntegerField(default=0, verbose_name='上级用户组') #0没有上级，填写菜单ID
	integral_int      = models.IntegerField(default=0, verbose_name='积分阈值')
	money_int         = models.IntegerField(default=0, verbose_name='余额阈值')
	totalmoney_int    = models.IntegerField(default=0, verbose_name='充值阈值')
	totalspend_int    = models.IntegerField(default=0, verbose_name='消费阈值')
	spread_int        = models.IntegerField(default=0, verbose_name='推广阈值')
	added_int         = models.IntegerField(default=0, verbose_name='每日新增')
	look_int          = models.IntegerField(default=0, verbose_name='每日查看')
	space_int         = models.IntegerField(default=0, verbose_name='每日上传')
	download_int      = models.IntegerField(default=0, verbose_name='每日下载')
	trial_bool        = models.BooleanField(default=False, verbose_name='自动过审')
	upload_bool       = models.BooleanField(default=False, verbose_name='上传权限')
	download_bool     = models.BooleanField(default=False, verbose_name='下载权限')
	menu_text         = models.TextField(blank=True, verbose_name='菜单权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	added_text        = models.TextField(blank=True, verbose_name='新增权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	delete_text       = models.TextField(blank=True, verbose_name='删除权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	update_text       = models.TextField(blank=True, verbose_name='修改权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|
	see_text          = models.TextField(blank=True, verbose_name='查看权限')#填写对应菜单ID, 格式：|菜单1||菜单2||菜单3|，PS:拥有菜单权限，就默认可以查看菜单，此查看权限是，方便设置此菜单下一些查看带星号手机之类的权限


class route(models.Model): #前台菜单表
	uid_int           = models.IntegerField(blank=False, unique=True, verbose_name='菜单id')
	name_str          = models.CharField(max_length=255, unique=True, blank=False, verbose_name='菜单名称')
	url_str           = models.CharField(max_length=255, blank=True, verbose_name='菜单URL')
	icon_str          = models.CharField(max_length=255, blank=True, default='fa fa-desktop', verbose_name='菜单图标')
	model_str         = models.CharField(max_length=255, blank=True, default='cover', verbose_name='菜单模型')# list=数据列表页面, form=表单提交页面 ，cover=无属性封面 ，url = 单独链接菜单
	superior_int      = models.IntegerField(default=0, verbose_name='上级菜单')
	sort_int          = models.IntegerField(default=0, verbose_name='菜单排序')
	integral_int      = models.IntegerField(default=0, verbose_name='积分门槛')
	money_int         = models.IntegerField(default=0, verbose_name='余额门槛')
	totalmoney_int    = models.IntegerField(default=0, verbose_name='充值门槛')
	totalspend_int    = models.IntegerField(default=0, verbose_name='消费门槛')
	spread_int        = models.IntegerField(default=0, verbose_name='推广门槛')
	display_bool      = models.BooleanField(default=True, verbose_name='菜单显示')


class dngroute(models.Model): # 后台菜单表
	uid_int           = models.IntegerField(blank=False, unique=True, verbose_name='菜单id')
	name_str          = models.CharField(max_length=255, unique=True, blank=False, verbose_name='菜单名称')
	url_str           = models.CharField(max_length=255, blank=True, verbose_name='菜单URL')
	icon_str          = models.CharField(max_length=255, blank=True, default='fa fa-desktop', verbose_name='菜单图标')
	model_str         = models.CharField(max_length=255, blank=True, default='cover', verbose_name='菜单模型')# list=数据列表页面, form=表单提交页面 ，cover=无属性封面 ，url = 单独链接菜单
	superior_int      = models.IntegerField(default=0, verbose_name='上级菜单')
	sort_int          = models.IntegerField(default=0, verbose_name='菜单排序')
	integral_int      = models.IntegerField(default=0, verbose_name='积分门槛')
	money_int         = models.IntegerField(default=0, verbose_name='余额门槛')
	totalmoney_int    = models.IntegerField(default=0, verbose_name='充值门槛')
	totalspend_int    = models.IntegerField(default=0, verbose_name='消费门槛')
	spread_int        = models.IntegerField(default=0, verbose_name='推广门槛')
	display_bool      = models.BooleanField(default=True, verbose_name='菜单显示')


class red(models.Model): #前台日志

	uid_int           = models.IntegerField(blank=False, verbose_name='会员id') # 所属会员的ID
	title_str         = models.CharField(max_length=255, blank=True, verbose_name='访问标题')
	url_str           = models.CharField(max_length=255, blank=True, verbose_name='访问网址')
	shebei_str        = models.CharField(max_length=255, blank=True, verbose_name='登录设备')
	ip_str            = models.CharField(max_length=255, blank=True, verbose_name='登录IP')
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

class dngred(models.Model): #后台日志

	uid_int           = models.IntegerField(blank=False, verbose_name='会员id') # 所属会员的ID
	title_str         = models.CharField(max_length=255, blank=True, verbose_name='访问标题')
	url_str           = models.CharField(max_length=255, blank=True, verbose_name='访问网址')
	shebei_str        = models.CharField(max_length=255, blank=True, verbose_name='登录设备')
	ip_str            = models.CharField(max_length=255, blank=True, verbose_name='登录IP')
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

class htmlsetup(models.Model): #前台设置

	title_str         = models.CharField(max_length=255, blank=False, default='DngAdmin开发框架', verbose_name='首页标题')
	keywords_str      = models.CharField(max_length=255, blank=True, default='DngAdmin开发框架', verbose_name='META关键词')
	description_str   = models.CharField(max_length=255, blank=True, default='DngAdmin框架3.0-基于python和Django的极速后台开发框架,为极速开发而生！', verbose_name='META描述')
	file_str          = models.CharField(max_length=255, blank=True, verbose_name='备案号') #备案号
	statistics_text   = models.TextField(blank=True, verbose_name='统计代码')#统计代码
	register_bool     = models.BooleanField(default=True, verbose_name='注册开关')

	inwidth_int       = models.IntegerField(default=120, verbose_name='最小表宽')
	wide_int          = models.IntegerField(default=800, verbose_name='弹窗宽度')
	high_int          = models.IntegerField(default=600, verbose_name='弹窗高度')
	limit_int         = models.IntegerField(default=15, verbose_name='默认条数')
	toolbar_bool      = models.BooleanField(default=True, verbose_name='头工具栏')
	skinline_str      = models.CharField(max_length=255, blank=True, verbose_name='表格边线')
	skinsize_str      = models.CharField(max_length=255, blank=True, verbose_name='表格缩放')
	page_bool         = models.BooleanField(default=True, verbose_name='底部分页')
	exports_str       = models.CharField(max_length=255, blank=True,default='exports', verbose_name='导出表格')
	print_str         = models.CharField(max_length=255, blank=True, default='print', verbose_name='打印表格')
	search_bool       = models.BooleanField(default=True, verbose_name='搜索表格')


class setup(models.Model): #后台设置

	setupname_str     = models.CharField(max_length=255, blank=False, default='DngAdmin开发框架', verbose_name='系统名称') #系统名称, 不许为空
	domain_str        = models.CharField(max_length=255, blank=False, verbose_name='系统域名') #系统域名, 不许为空
	file_str          = models.CharField(max_length=255, blank=True, verbose_name='备案号') #备案号
	edition_str       = models.CharField(max_length=255, blank=True, default='DngAdmin版本3.0', verbose_name='版本号') #版本号
	statistics_text   = models.TextField(blank=True, verbose_name='统计代码')#统计代码

	inwidth_int       = models.IntegerField(default=160, verbose_name='最小表宽')
	wide_int          = models.IntegerField(default=800, verbose_name='弹窗宽度')
	high_int          = models.IntegerField(default=600, verbose_name='弹窗高度')
	limit_int         = models.IntegerField(default=15, verbose_name='默认条数')
	toolbar_bool      = models.BooleanField(default=True, verbose_name='头工具栏')
	skinline_str      = models.CharField(max_length=255, blank=True, verbose_name='表格边线')
	skinsize_str      = models.CharField(max_length=255, blank=True, verbose_name='表格缩放')
	page_bool         = models.BooleanField(default=True, verbose_name='底部分页')
	exports_str       = models.CharField(max_length=255, blank=True,default='exports', verbose_name='导出表格')
	print_str         = models.CharField(max_length=255, blank=True, default='print', verbose_name='打印表格')
	search_bool       = models.BooleanField(default=True, verbose_name='搜索表格')

class protect(models.Model): #前台安全

	uid_int           = models.IntegerField(blank=False, unique=True, verbose_name='安全ID')  # 安全策略的ID, 设置不能为空，不可重复
	entrance_str      = models.CharField(max_length=255, blank=True, verbose_name='安全入口') #后台安全入口
	prescription_int  = models.IntegerField(blank=True, default=86400, verbose_name='Cookies时效') #Cookies时效, 单位毫秒，默认24小时
	salt_str          = models.CharField(max_length=255, blank=True, verbose_name='加密盐') #解析COOKIE的加密盐
	requests_int      = models.IntegerField(blank=False, default=5, verbose_name='密错次数') #防暴力破解，超过次数限制登录
	psdreq_int        = models.IntegerField(blank=False, default=1, verbose_name='冻结时间')  # 密码错误后冻结，单位小时
	graphic_bool      = models.BooleanField(default=False, verbose_name='图形验开关')  # 图形验证码开关，False=关闭 True=开启
	station_bool      = models.BooleanField(default=False, verbose_name='验证感知')  # 跨站POST开关，False=关闭 True=开启
	useragent_str     = models.CharField(max_length=255, blank=True, verbose_name='允许设备') #允许useragent设备，分割线|分割
	area_str          = models.CharField(max_length=255, blank=True, verbose_name='允许地区') #允许登录得地区，分割线|分割
	tongshi_bool      = models.BooleanField(default=False, verbose_name='同时在线') #同时在线开关，False=不允许同时 True=允许同时
	sms_bool          = models.BooleanField(default=False, verbose_name='短信验证') #短信验证开关，False=不开 True=开启
	iptxt_text        = models.TextField(blank=True, verbose_name='禁止IP')#富文本超大字符串, |符号分割

class security(models.Model): #后台安全

	uid_int           = models.IntegerField(blank=False, unique=True, verbose_name='安全ID')  # 安全策略的ID, 设置不能为空，不可重复
	entrance_str      = models.CharField(max_length=255, blank=True, verbose_name='安全入口') #后台安全入口
	prescription_int  = models.IntegerField(blank=True, default=86400, verbose_name='Cookies时效') #Cookies时效, 单位毫秒，默认24小时
	salt_str          = models.CharField(max_length=255, blank=True, verbose_name='加密盐') #解析COOKIE的加密盐
	requests_int      = models.IntegerField(blank=False, default=5, verbose_name='密错次数') #防暴力破解，超过次数限制登录
	psdreq_int        = models.IntegerField(blank=False, default=1, verbose_name='冻结时间')  # 密码错误后冻结，单位小时
	graphic_bool      = models.BooleanField(default=False, verbose_name='图形验开关')  # 图形验证码开关，False=关闭 True=开启
	station_bool      = models.BooleanField(default=False, verbose_name='验证感知')  # 跨站POST开关，False=关闭 True=开启
	useragent_str     = models.CharField(max_length=255, blank=True, verbose_name='允许设备') #允许useragent设备，分割线|分割
	area_str          = models.CharField(max_length=255, blank=True, verbose_name='允许地区') #允许登录得地区，分割线|分割
	tongshi_bool      = models.BooleanField(default=False, verbose_name='同时在线') #同时在线开关，False=不允许同时 True=允许同时
	sms_bool          = models.BooleanField(default=False, verbose_name='短信验证') #短信验证开关，False=不开 True=开启
	iptxt_text        = models.TextField(blank=True, verbose_name='禁止IP')#富文本超大字符串, |符号分割

class mail(models.Model): #邮件设置

	type_str          = models.CharField(max_length=255, blank=True, verbose_name='邮件发送方式')
	host_str          = models.CharField(max_length=255, blank=True, verbose_name='SMTP服务器')
	port_str          = models.CharField(max_length=255, blank=True, verbose_name='SMTP端口')
	user_str          = models.CharField(max_length=255, blank=True, verbose_name='SMTP用户名')
	pass_str          = models.CharField(max_length=255, blank=True, verbose_name='SMTP密码')
	verify_str        = models.CharField(max_length=255, blank=True, verbose_name='SMTP验证方式')
	from_str          = models.CharField(max_length=255, blank=True, verbose_name='发件人邮箱')
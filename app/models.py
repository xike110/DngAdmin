from django.db import models
import random#随机模块
#——————————一键生成后缀规范——————————————————
# 静态框表名_id后缀(生成静态框,不可修改，验证规则=是否为数字，不能重复，不能为空值)  数据库类型==models.IntegerField_整形数字
# 文本框表名_str后缀(生成文本框,验证规则=填写不能为空) 数据库类型==models.CharField_字符串类型
# 禁用文本框表名_stop后缀(禁止填写,禁止修改) 数据库类型==models.CharField_字符串类型
# 密码框表名_psd后缀(禁用文本框,验证规则=密码必须6到12位，且不能出现空格，存时候会默认转MD5)  数据库类型==models.CharField_字符串类型
# 手机表名_phone后缀(生成文本框,验证规则=是否为手机号) 数据库类型==models.CharField_字符串类型
# 邮箱框表名_email后缀(生成文本框,验证规则=是否为邮箱) 数据库类型==models.CharField_字符串类型
# 身份证框表名_entity后缀(生成文本框,验证规则=18位数字身份证,不支持字母身份证) 数据库类型==models.CharField_字符串
# 数字框表名_int后缀(生成数字框,验证规则=只能输入非负整数，做大输入1个亿)  数据库类型==models.IntegerField整形数字
# 下拉框表名_xiala后缀(生成下拉框,验证规则=默认下拉值,default默认值必须写)  数据库类型==models.CharField_字符串 添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
# 选择框表名_xuanze后缀(生成选择框,验证规则=默认选择值,default默认值必须写) 数据库类型==models.CharField_字符串 添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
# 竖单选框表名_shudanxuan后缀(生成竖单选框,验证规则=默认选择值,default默认值必须写) 数据库类型==models.CharField_字符串 添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
# 横单选框表名_hengdanxuan后缀(生成横单选框,验证规则=默认选择值,default默认值必须写) 数据库类型==models.CharField_字符串 添加好选择元组  choices=(('nan','男'),('nv','女')),default='男'
# 开关框表名_bool后缀(生成开关框)  数据库类型==models.BooleanField_布尔真假类型
# 日期框表名_years后缀(生成日期框，验证规则=是否为时间)  数据库类型==DateTimeField 时间类型 格式=日期,(2099-12-28 00:00:00)
# 日期时间框表名_datetime后缀(生成日期+时间框，验证规则=是否为时间) 数据库类型==DateTimeField 时间类型 格式=日期+时间,(2099-12-28 23:59:59)
# 富文本框表名_text后缀(生成超大文本框,验证规则=填写不能为空，字数限制1万以内)  数据库类型==models.TextField_富文本
# 自动创建时间create_time  完整默认字段名称（请规范写，不然会前端要求填写创建时间）
# 自动更新时间update_time  完整默认字段名称（请规范写，不然会前端要求填写更新时间）

#————————————————字段属性说明——————————————
# verbose_name=字段备注
# blank=是否为必填项blank=False 等于必填，如果 blank=True，表示可以不填
# max_length=字符串的最大值,默认设置255
# unique=True=如果为True, 数值不能重复，这个字段在表中必须有唯一值
# default=默认填写值
# choices=元组选择  例子：models.CharField(max_length=255,choices=(('male','男'),('female','女')),default='male',verbose_name='性别')
# DatetimeField、DateField、TimeField这个三个时间字段独有
#——————————注意事项——————————————————

# 注意事项：(一) 不要用自增id，来作为用户ID或者业务id，不少新手都会这种方法，会使得业务与id生成强耦合，导致id生成算法难以升级，未来分布式数据库，和分表都会麻烦（如果准备分布式ID主键建议采用UUID,有条件采用雪花算法），
# 注意事项：(二) 不要修改已经建立的数据库字段，会带来未知风险，建议对字段新增，不要删除修改系统已经存在的数据库字段，
# 注意事项：(三) 创建字段名称记得带类型后缀，方便前台识别，生成对应表单输入样式
# 注意事项：(四) 你不确定未来会迁移什么类型数据库，为了保证通用，尽量全部小写，慎用驼峰命名法，数据库高手忽略此条

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
	frozen_bool       = models.BooleanField(default=True, verbose_name='登录开关') #账号限制登录，False=没有禁止 True=账号禁止
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
	frozen_bool       = models.BooleanField(default=True, verbose_name='登陆开关') #账号限制登录，False=没有禁止 True=账号禁止
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
	model_str         = models.CharField(max_length=255, blank=True, default='cover', verbose_name='菜单模型')# list=数据列表页面, form=表单提交页面 ，cover=无属性封面 ，url = 单独链接菜单，none = 空白页
	superior_int      = models.IntegerField(default=0, verbose_name='上级菜单')
	sort_int          = models.IntegerField(default=0, verbose_name='菜单排序')
	integral_int      = models.IntegerField(default=0, verbose_name='积分门槛')
	money_int         = models.IntegerField(default=0, verbose_name='余额门槛')
	totalmoney_int    = models.IntegerField(default=0, verbose_name='充值门槛')
	totalspend_int    = models.IntegerField(default=0, verbose_name='消费门槛')
	spread_int        = models.IntegerField(default=0, verbose_name='推广门槛')
	display_bool      = models.BooleanField(default=True, verbose_name='菜单显示')
	prove_bool        = models.BooleanField(default=True, verbose_name='权限验证')
	seotirle_str      = models.CharField(max_length=255, blank=True, verbose_name='SEO标题')
	keywords_str 	  = models.CharField(max_length=255, blank=True, verbose_name='SEO关键词')
	description_str   = models.CharField(max_length=255, blank=True, verbose_name='SEO描述')


class dngroute(models.Model): # 后台菜单表
	uid_int           = models.IntegerField(blank=False, unique=True, verbose_name='菜单id')
	name_str          = models.CharField(max_length=255, unique=True, blank=False, verbose_name='菜单名称')
	url_str           = models.CharField(max_length=255, blank=True, verbose_name='菜单URL')
	icon_str          = models.CharField(max_length=255, blank=True, default='fa fa-desktop', verbose_name='菜单图标')
	model_str         = models.CharField(max_length=255, blank=True, default='cover', verbose_name='菜单模型')# list=数据列表页面, form=表单提交页面 ，cover=无属性封面 ，url = 单独链接菜单，none = 空白页
	superior_int      = models.IntegerField(default=0, verbose_name='上级菜单')
	sort_int          = models.IntegerField(default=0, verbose_name='菜单排序')
	integral_int      = models.IntegerField(default=0, verbose_name='积分门槛')
	money_int         = models.IntegerField(default=0, verbose_name='余额门槛')
	totalmoney_int    = models.IntegerField(default=0, verbose_name='充值门槛')
	totalspend_int    = models.IntegerField(default=0, verbose_name='消费门槛')
	spread_int        = models.IntegerField(default=0, verbose_name='推广门槛')
	display_bool      = models.BooleanField(default=True, verbose_name='菜单显示')
	prove_bool        = models.BooleanField(default=True, verbose_name='权限验证')
	seotirle_str      = models.CharField(max_length=255, blank=True, verbose_name='SEO标题')
	keywords_str 	  = models.CharField(max_length=255, blank=True, verbose_name='SEO关键词')
	description_str   = models.CharField(max_length=255, blank=True, verbose_name='SEO描述')



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

	title_str         = models.CharField(max_length=255, blank=False, default='DngAdmin后台系统-为极速开发而生！', verbose_name='首页SEO标题')
	logotitle_str     = models.CharField(max_length=255, blank=False, default='DNG系统', verbose_name='品牌名称')
	keywords_str      = models.CharField(max_length=255, blank=True, default='DngAdmin后台系统', verbose_name='META关键词')
	description_str   = models.CharField(max_length=255, blank=True, default='DngAdmin后台系统1.0-基于python和Django原生开发,为极速开发而生！', verbose_name='META描述')
	file_str          = models.CharField(max_length=255, blank=True, verbose_name='备案号') #备案号
	statistics_text   = models.TextField(blank=True, verbose_name='统计代码')#统计代码
	register_bool     = models.BooleanField(default=True, verbose_name='注册开关')
	http_bool         = models.BooleanField(default=True, verbose_name='网站开关')


	inwidth_int       = models.IntegerField(default=120, verbose_name='最小表宽')
	wide_int          = models.IntegerField(default=800, verbose_name='弹窗宽度')
	high_int          = models.IntegerField(default=600, verbose_name='弹窗高度')
	limit_int         = models.IntegerField(default=20, verbose_name='默认条数')
	toolbar_bool      = models.BooleanField(default=True, verbose_name='头工具栏')
	skinline_str      = models.CharField(max_length=255, blank=True, verbose_name='表格边线')
	skinsize_str      = models.CharField(max_length=255, blank=True, default='sm',verbose_name='表格缩放')
	page_bool         = models.BooleanField(default=True, verbose_name='底部分页')
	exports_str       = models.CharField(max_length=255, blank=True,default='exports', verbose_name='导出表格')
	print_str         = models.CharField(max_length=255, blank=True, default='print', verbose_name='打印表格')
	search_bool       = models.BooleanField(default=True, verbose_name='搜索表格')


class setup(models.Model): #后台设置

	setupname_str     = models.CharField(max_length=255, blank=False, default='DngAdmin后台系统', verbose_name='系统名称') #系统名称, 不许为空
	domain_str        = models.CharField(max_length=255, blank=False, verbose_name='系统域名') #系统域名, 不许为空
	file_str          = models.CharField(max_length=255, blank=True, verbose_name='备案号') #备案号
	edition_str       = models.CharField(max_length=255, blank=True, default='DngAdmin版本1.0', verbose_name='版本号') #版本号
	statistics_text   = models.TextField(blank=True, verbose_name='统计代码')#统计代码

	inwidth_int       = models.IntegerField(default=160, verbose_name='最小表宽')
	wide_int          = models.IntegerField(default=800, verbose_name='弹窗宽度')
	high_int          = models.IntegerField(default=600, verbose_name='弹窗高度')
	limit_int         = models.IntegerField(default=20, verbose_name='默认条数')
	toolbar_bool      = models.BooleanField(default=True, verbose_name='头工具栏')
	skinline_str      = models.CharField(max_length=255, blank=True, verbose_name='表格边线')
	skinsize_str      = models.CharField(max_length=255, blank=True, default='sm',verbose_name='表格缩放')
	page_bool         = models.BooleanField(default=True, verbose_name='底部分页')
	exports_str       = models.CharField(max_length=255, blank=True,default='exports', verbose_name='导出表格')
	print_str         = models.CharField(max_length=255, blank=True, default='print', verbose_name='打印表格')
	search_bool       = models.BooleanField(default=True, verbose_name='搜索表格')

class protect(models.Model): #前台安全

	uid_int           = models.IntegerField(blank=False, unique=True, verbose_name='安全ID')  # 安全策略的ID, 设置不能为空，不可重复
	entrance_str      = models.CharField(max_length=255, blank=True, verbose_name='安全入口') #后台安全入口
	prescription_int  = models.IntegerField(blank=True, default=86400, verbose_name='Cookies时效') #Cookies时效, 单位毫秒，默认24小时
	salt_str          = models.CharField(max_length=255, blank=True, verbose_name='加密盐') #解析COOKIE的加密盐
	apipsd_str        = models.CharField(max_length=255, blank=True, verbose_name='Api密码')  # 解析COOKIE的加密盐
	tokenpsd_str      = models.CharField(max_length=255, blank=True, verbose_name='Token密钥')  # 解析COOKIE的加密盐
	requests_int      = models.IntegerField(blank=False, default=10, verbose_name='密错次数') #防暴力破解，超过次数限制登录
	psdreq_int        = models.IntegerField(blank=False, default=24, verbose_name='冻结时间')  # 密码错误后冻结，单位小时
	graphic_bool      = models.BooleanField(default=True, verbose_name='图码验证')  # 图形验证码开关，False=关闭 True=开启
	station_bool      = models.BooleanField(default=False, verbose_name='邮件验证')  # 跨站POST开关，False=关闭 True=开启
	sms_bool          = models.BooleanField(default=False, verbose_name='短信验证') #短信验证开关，False=不开 True=开启
	useragent_str     = models.CharField(max_length=255, blank=True, verbose_name='允许设备') #允许useragent设备，分割线|分割
	area_str          = models.CharField(max_length=255, blank=True, verbose_name='允许地区') #允许登录得地区，分割线|分割
	tongshi_bool      = models.BooleanField(default=False, verbose_name='同时在线') #同时在线开关，False=不允许同时 True=允许同时
	iptxt_text        = models.TextField(blank=True, verbose_name='禁止IP')#富文本超大字符串, |符号分割

class security(models.Model): #后台安全

	uid_int           = models.IntegerField(blank=False, unique=True, verbose_name='安全ID')  # 安全策略的ID, 设置不能为空，不可重复
	entrance_str      = models.CharField(max_length=255, blank=True, verbose_name='安全入口') #后台安全入口
	prescription_int  = models.IntegerField(blank=True, default=86400, verbose_name='Cookies时效') #Cookies时效, 单位毫秒，默认24小时
	salt_str          = models.CharField(max_length=255, blank=True, verbose_name='加密盐') #解析COOKIE的加密盐
	apipsd_str        = models.CharField(max_length=255, blank=True, verbose_name='Api密码')  # 解析COOKIE的加密盐
	tokenpsd_str      = models.CharField(max_length=255, blank=True, verbose_name='Token密钥')  # 解析COOKIE的加密盐
	requests_int      = models.IntegerField(blank=False, default=10, verbose_name='密错次数') #防暴力破解，超过次数限制登录
	psdreq_int        = models.IntegerField(blank=False, default=24, verbose_name='冻结时间')  # 密码错误后冻结，单位小时
	graphic_bool      = models.BooleanField(default=True, verbose_name='图码验证')  # 图形验证码开关，False=关闭 True=开启
	station_bool      = models.BooleanField(default=False, verbose_name='邮件验证')  # 跨站POST开关，False=关闭 True=开启
	sms_bool          = models.BooleanField(default=False, verbose_name='短信验证') #短信验证开关，False=不开 True=开启
	useragent_str     = models.CharField(max_length=255, blank=True, verbose_name='允许设备') #允许useragent设备，分割线|分割
	area_str          = models.CharField(max_length=255, blank=True, verbose_name='允许地区') #允许登录得地区，分割线|分割
	tongshi_bool      = models.BooleanField(default=False, verbose_name='同时在线') #同时在线开关，False=不允许同时 True=允许同时
	iptxt_text        = models.TextField(blank=True, verbose_name='禁止IP')#富文本超大字符串, |符号分割

class mail(models.Model): #邮件设置
	mail_id           = models.IntegerField(blank=False, unique=True, verbose_name='邮件ID')
	type_str          = models.CharField(max_length=255, blank=True, default='POP3/SMTP',verbose_name='邮件发送方式')
	host_str          = models.CharField(max_length=255, blank=True, default='smtp.qq.com', verbose_name='SMTP服务器')
	port_str          = models.CharField(max_length=255, blank=True, default='587',verbose_name='SMTP端口')
	pass_str          = models.CharField(max_length=255, blank=True, verbose_name='SMTP授权码')
	from_str          = models.CharField(max_length=255, blank=True, verbose_name='发件人邮箱')
	requests_int      = models.IntegerField(blank=False, default=30, verbose_name='用户每日邮件上限')
	youxiao_int       = models.IntegerField(blank=False, default=180, verbose_name='有效时间:秒')
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 后台注册时间
	update_time       = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 最后一次登录时间

class sms(models.Model): #短信设置
	mail_id           = models.IntegerField(blank=False, unique=True, verbose_name='短信ID')
	ali_shudanxuan	  = models.CharField(max_length=255, choices=(('阿里市场-国阳网','阿里市场-国阳网'),('阿里市场-聚美智数','阿里市场-聚美智数'),('阿里市场-鼎信科技','阿里市场-鼎信科技'),('阿里市场-云智信','阿里市场-云智信'),('阿里市场-深智科技','阿里市场-深智科技'),('自定义短信模块','自定义短信模块')),default='阿里市场-国阳网', verbose_name='短信供应商',)
	appcode_str       = models.CharField(max_length=255, blank=True, verbose_name='阿里AppCode')
	requests_int      = models.IntegerField(blank=False, default=20, verbose_name='用户每日短信上限')
	youxiao_int       = models.IntegerField(blank=False, default=180, verbose_name='有效时间:秒')
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 后台注册时间
	update_time       = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 最后一次登录时间

class pluguser(models.Model): #插件设置
	plug_id 	      = models.IntegerField(blank=False, unique=True,  verbose_name='用户ID')
	plugname_stop     = models.CharField(max_length=255, blank=True,verbose_name='DNG账号')
	pluggroup_stop    = models.CharField(max_length=255, blank=True,verbose_name='用户组')
	mobile_stop       = models.CharField(max_length=255, blank=True, verbose_name='手机号')  # 手机号接收短信等
	money_stop        = models.IntegerField(default=0, verbose_name='余额')  # 余额，默认值为0，不支持小数点
	integral_stop     = models.IntegerField(default=0, verbose_name='积分')  # 积分，默认值为0，不支持小数点
	spread_stop       = models.IntegerField(default=0, verbose_name='推广')  # 推广，默认值为0，不支持小数点
	appcode_stop      = models.CharField(max_length=255, blank=True, verbose_name='AppCode密钥')
	cookie_stop       = models.CharField(max_length=255, blank=True, verbose_name='Cookie密钥')
	token_stop        = models.CharField(max_length=255, blank=True, verbose_name='Token密钥')
	lockcode_stop     = models.CharField(max_length=255, blank=True, verbose_name='机器码')
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间') #后台注册时间
	update_time       = models.DateTimeField(auto_now=True, verbose_name='更新时间')#最后一次登录时间

class formdemo(models.Model): #表单组件演示
	demoid_id		  = models.IntegerField(blank=False, unique=True, verbose_name='表单ID')
	wenben_str	      = models.CharField(max_length=255, blank=True, verbose_name='文本框')
	jinyong_stop      = models.CharField(max_length=255, blank=True, default='新手用户组',verbose_name='禁用框')
	mima_psd		  = models.CharField(max_length=255, blank=True, verbose_name='密码框')
	shouji_phone	  = models.CharField(max_length=255, blank=True, verbose_name='手机框')
	youjian_email     = models.CharField(max_length=255, blank=True, verbose_name='邮件框')
	shenfen_entity  = models.CharField(max_length=255, blank=True, verbose_name='身份证框')
	shuzi_int         = models.IntegerField(blank=True, default=0, verbose_name='数字框')
	xuanze_xiala	  = models.CharField(max_length=255, choices=(('下拉选项 01','下拉选项 01'),('下拉选项 02','下拉选项 02'),('下拉选项 03','下拉选项 03'),('下拉选项 04','下拉选项 04')),default='下拉选项 01', verbose_name='下拉框',)
	xuanze_xuanze     = models.CharField(max_length=255, choices=(('选择选项 01','选择选项 01'),('选择选项 02','选择选项 02'),('选择选项 03','选择选项 03'),('选择选项 04','选择选项 04')),default='选择选项 01', verbose_name='选择框', )
	shu_shudanxuan    = models.CharField(max_length=255, choices=(('竖单选项 01','竖单选项 01'),('竖单选项 02','竖单选项 02'),('竖单选项 03','竖单选项 03'),('竖单选项 04','竖单选项 04')),default='竖单选项 01', verbose_name='竖单选框', )
	heng_hengdanxuan  = models.CharField(max_length=255, choices=(('横单选项 01','横单选项 01'),('横单选项 02','横单选项 02'),('横单选项 03','横单选项 03'),('横单选项 04','横单选项 04')),default='横单选项 01', verbose_name='横单选框', )
	kaiguan_bool      = models.BooleanField(default=False, verbose_name='启动开关')
	riqi_years        = models.DateTimeField(blank=True, default='2021-06-01', verbose_name='日期框')
	datetime_datetime = models.DateTimeField(blank=True, default='2099-12-28 23:59:59', verbose_name='日期时间框')
	fuwenben_text     = models.TextField(blank=True,verbose_name='富文本框')
	create_time       = models.DateTimeField(auto_now_add=True, verbose_name='创建时间') #后台注册时间
	update_time       = models.DateTimeField(auto_now=True, verbose_name='更新时间')#最后一次登录时间

class shenbao(models.Model): #故障申报演示
	sb_id = models.IntegerField(blank=False, unique=True, verbose_name='申报ID')
	name_str = models.CharField(max_length=255, blank=True, verbose_name='申报人')
	yonghuzu_stop = models.CharField(max_length=255, blank=True, default='维护组', verbose_name='申报组')
	shouji_phone = models.CharField(max_length=255, blank=True, verbose_name='手机')
	youjian_email = models.CharField(max_length=255, blank=True, verbose_name='邮件')
	xuanze_xiala = models.CharField(max_length=255, choices=(('营销部', '营销部'), ('技术部', '技术部'), ('售后部', '售后部'), ('后勤部', '后勤部')), default='营销部',verbose_name='故障部门', )
	xuanze_xuanze = models.CharField(max_length=255, choices=(('路由器', '路由器'), ('交换机', '交换机'), ('电脑', '电脑'), ('打印机', '打印机')), default='路由器',verbose_name='故障设备', )
	shu_shudanxuan = models.CharField(max_length=255, choices=(('李老师', '李老师'), ('罗老师', '罗老师'), ('金老师', '金老师'), ('宋老师', '宋老师')), default='李老师',verbose_name='故障联络人', )
	heng_hengdanxuan = models.CharField(max_length=255, choices=(('网络故障', '网络故障'), ('电力故障', '电力故障'), ('通信故障', '通信故障'), ('显示故障', '显示故障')), default='网络故障',verbose_name='故障项目', )
	kaiguan_bool = models.BooleanField(default=False, verbose_name='联系开关')
	riqi_years = models.DateTimeField(blank=True, default='2021-06-01', verbose_name='故障日期')
	fuwenben_text = models.TextField(blank=True, verbose_name='故障详细描述')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')  # 后台注册时间
	update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 最后一次登录时间



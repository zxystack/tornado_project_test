# coding:utf-8

import logging
import constants
import random
import re

from .BaseHandler import BaseHandler
from utils.captcha.captcha import captcha
from utils.response_code import RET
from libs.yuntongxun.CCP import ccp
from utils.session import Session

class ImageCodeHandler(BaseHandler):
    """"""
    def get(self):
        code_id = self.get_argument("codeid")
        pre_code_id = self.get_argument("pcodeid")
        if pre_code_id:
            try:
                self.redis.delete("image_code_%s" % pre_code_id)
            except Exception as e:
                logging.error(e)
        # name 图片验证码名称
        # text 图片验证码文本
        # image 图片验证码二进制数据
        name, text, image = captcha.generate_captcha()
        try:
            self.redis.setex("image_code_%s" % code_id, constants.IMAGE_CODE_EXPIRES_SECONDS, text)
        except Exception as e:
            logging.error(e)
            self.write("")
        else:
            self.set_header("Content-Type", "image/jpg")
            self.write(image)


class SMSCodeHandler(BaseHandler):
    """"""
    def post(self):
        # 获取参数
        mobile = self.json_args.get("mobile") 

        print mobile
        image_code_id = self.json_args.get("image_code_id") 
        print image_code_id
        image_code_text = self.json_args.get("image_code_text") 
        if not all((mobile, image_code_id, image_code_text)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整")) 
        if not re.match(r"1\d{10}", mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg="手机号错误")) 
        # 判断图片验证码
        try:
            real_image_code_text = self.redis.get("image_code_%s" % image_code_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="查询出错"))
        if not real_image_code_text:
            return self.write(dict(errno=RET.NODATA, errmsg="验证码已过期！"))
        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errno=RET.DATAERR, errmsg="验证码错误！"))
        # 若成功：
        # 生成随机验证码
        sms_code = "%04d" % random.randint(0, 9999)
        print sms_code
        try:
            self.redis.setex("sms_code_%s" % mobile, constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
            print 'aaaaaaa'
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="生成短信验证码错误"))
        # 发送短信
        try:
            ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60], 1)
            # 需要判断返回值，待实现
        except Exception as e:
            logging.error(e)
            print 'ccccccc'
            return self.write(dict(errno=RET.THIRDERR, errmsg="发送失败！"))
            
        self.write(dict(errno=RET.OK, errmsg="OK"))



class RegisterHandler(BaseHandler):
    def post(self):
        mobile = self.json_args.get('mobile')
        print mobile
        password = self.json_args.get('passwd')
        print password
        
        phoneCode = self.json_args.get('phoneCode')
        print phoneCode

        
        if not all((mobile, password, phoneCode)):
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数不完整")) 
        if not re.match(r"1\d{10}", mobile):
            return self.write(dict(errno=RET.PARAMERR, errmsg="手机号错误")) 
        if not re.match(r'^[A-Za-z][a-zA-Z0-9]',password):
            return self.write(dict(errno=RET.PARAMERR,errmsg='密码格式不正确'))
        
        if len(password)<6 or len(password)>16:
            return self.write(dict(errno=RET.PARAMERR,errmsg='密码位数不正确'))
        #从redis中获取对应手机号的验证码
        re_phoneCode = self.redis.get("sms_code_%s" % mobile)
        print re_phoneCode
        if phoneCode != re_phoneCode:
            self.write(dict(errno=RET.PARAMERR,errmsg='验证码输入错误'))
        try:
            all_user = self.db.query('select up_mobile from ih_user_profile')
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg="数据库错误"))
      
        # if mobile in all_user.values():
        #     return self.write(dict(errno=RET.DATAERR,errmsg='用户已经存在'))
        for i in all_user:
            if str(mobile) ==i.up_mobile:
                return self.write(dict(errno=RET.DATAERR,errmsg='用户已经存在'))
        #验证成功之后 存入mysql数据库
        self.write(dict(errno=RET.OK, errmsg="OK"))
        self.db.execute("insert into ih_user_profile(up_mobile, up_passwd, up_name) values(%s, %s, %s)",mobile,password,mobile )

class LoginHandler(BaseHandler):
    def post(self):
        mobile = self.json_args.get('mobile')
     
        passwd = self.json_args.get('passwd')
       
        # if not re.match(r"1\d{10}", mobile):
        #     return self.write(dict(errno=RET.PARAMERR, errmsg="手机号错误"))
        # if not re.match(r'^[A-Za-z][a-zA-Z0-9]',password):
        #     return self.write(dict(errno=RET.PARAMERR,errmsg='密码格式不正确'))
        try:
            rets = self.db.query('select up_user_id,up_mobile,up_passwd from ih_user_profile where up_mobile=%s',mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmg="数据库错误"))
        
        if rets:
            # print(mobile == str(rets[0].up_mobile))
    
            if mobile == str(rets[0].up_mobile) and passwd== str(rets[0].up_passwd):
                try:
                    # print(rets[0].up_mobile)
                    self.session = Session(self)
                    # print(1111111111111)
                    # self.session = Session(self)
                    self.session.data['name1']  = rets[0].up_mobile
                    # print(1111111111111)
                    self.session.data['up_mobile1'] = rets[0].up_mobile
                    # print('qqqqqqqqqq')
                    print self.session.data['up_mobile1']
                    self.session.save()
                    
                except Exception as e:
                    logging.error(e)
                    return self.write(dict(errno=RET.DATAERR,errmg = '数据库错误'))
                return self.write(dict(errno=RET.OK,errmg='OK'))


            else:
                return self.write(dict(errno=RET.DATAERR,errmg='账号或密码错误'))
        else:
            return self.write(dict(errno=RET.DATAERR,errmg='用户不存在'))

        

class LoginCheckHandler(BaseHandler):

    def get(self):
       
        # print self.get_current_user()
        if self.get_current_user():
        # if True:
            print self.session.data.get("up_mobile1")
            # self.write(dict(errno='1',data={'name':self.session.data.get('up_mobile1')}))
            self.write({"errno":'1',"data":{"name":self.session.data.get("up_mobile1")}})
            print('qqqqqqqqq')
        else:
            self.write(dict(errno='0',errmg='用户未登录'))


class LogoutHandler(BaseHandler):
    def get (self):
        print('11111111')
        self.session = Session(self)
        try:
            self.session.clear()
        except Exception as e:
            logging.error(e)
            self.write(dict(errno='0',errmg='数据库错误'))
        else:
            return self.write(dict(errno='1',errmg='退出成功'))

#我的爱家页面获取个人信息
class UserInfoHandler(BaseHandler):
    @require_logined
    def post(self):
        mobile = self.session.data.get('up_mobile1')
        try:
            rets = self.db.query(('select up_name,up_mobile from ih_user_profile where up_mobile=%s',mobile))
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno='0',errmg='数据库错误'))
        else:
            return self.write({'errno':'1',"data":{'username':rets[0].up_name,'mobile':rets[0].up_mobile}})



#上传图片
# class AvatarHandler(BaseHandler):
#     """头像"""
#     @require_logined
#     def post(self):
#         user_id = self.session.data["user_id"]
#         try:
#             avatar = self.request.files["avatar"][0]["body"]
#         except Exception as e:
#             logging.error(e)
#             return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))
#         try:
#             img_name = storage(avatar)
#         except Exception as e:
#             logging.error(e)
#             img_name = None
#         if not img_name:
#             return self.write({"errno":RET.THIRDERR, "errmsg":"qiniu error"})
#         try:
#             ret = self.db.execute("update ih_user_profile set up_avatar=%s where up_user_id=%s", img_name, user_id)
#         except Exception as e:
#             logging.error(e)
#             return self.write({"errno":RET.DBERR, "errmsg":"upload failed"})
#         img_url = image_url_prefix + img_name
#         self.write({"errno":RET.OK, "errmsg":"OK", "url":img_url})

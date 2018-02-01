# coding:utf-8

import os

from handlers import Passport, VerifyCode
from handlers.BaseHandler import StaticFileHandler

handlers = [
	(r'/api/profile',VerifyCode.UserInfoHandler),
	(r'/api/logout',VerifyCode.LogoutHandler),
	(r'/api/logincheck',VerifyCode.LoginCheckHandler),
	(r'/api/login',VerifyCode.LoginHandler),
	(r'/api/register',VerifyCode.RegisterHandler),
    (r"/api/imagecode", VerifyCode.ImageCodeHandler),
    (r"/api/smscode", VerifyCode.SMSCodeHandler),
    (r"/(.*)", StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]
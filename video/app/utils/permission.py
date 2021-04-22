# coding:utf8

#编写装饰器
import functools
from django.shortcuts import redirect,reverse

def dashboard_auth(func):

    @functools.wraps(func)
    def wrapper(self,request,*args,**kwargs):
        user = request.user

        if not user.is_authenticated or not user.is_superuser:
            return redirect(f'{reverse("dashboard_login")}?to={request.path}')
            
        return func(self,request,*args,**kwargs)
    return wrapper 
 
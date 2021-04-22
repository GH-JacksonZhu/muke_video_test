# coding:utf8
from django.views.generic import View #用于创建视图
from app.libs.base_render import render_to_response #导入mako
from django.shortcuts import redirect,reverse #用于重定向到某网页

from django.contrib.auth import login,logout,authenticate #用于登陆，注销，验证
from django.contrib.auth.models import User #使用数据库的User

from django.core.paginator import Paginator #用于分页

from app.utils.permission import dashboard_auth

class Login(View):
    TEMPLATE = '/dashboard/auth/login.html'

    def get(self,request):
        data = {}

        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))

        to = request.GET.get('to','')
        data['to'] = to

        data['error'] = ''
        return render_to_response(request,self.TEMPLATE,data=data)

    def post(self,request):
        print(1)
        data = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        to = request.GET.get('to','')

        exists = User.objects.filter(username=username).exists()
        if not exists: #判断用户是否存在
            data = {'error':'用户不存在'}
            return render_to_response(request,self.TEMPLATE,data=data)

        user = authenticate(username=username,password=password)
        if not user: #判断
            data['error'] = '密码错误'
            return render_to_response(request,self.TEMPLATE,data=data)

        if not user.is_superuser:
            data['error'] = '你无权登录'
            return render_to_response(request,self.TEMPLATE,data=data)
        login(request,user)

        if to:
            return redirect(to)
            
        return redirect(reverse('dashboard_index'))

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('dashboard_login'))

class AdminManager(View):
    TEMPLATE = '/dashboard/auth/admin.html'

    @dashboard_auth
    def get(self,request):
        data = {}
        
        # users = User.objects.filter(is_superuser=True) #区分是否是管理员
        users = User.objects.all()


        #用于分页
        page = request.GET.get('page',1) #获取请求的页数
        p = Paginator(users,2) #设置每页两个数据
        current_page = p.get_page(int(page)).object_list #获取当前page页的数据

        total_page = p.num_pages #查看一共有多少页数
        if int(page) <= 1:
            page=1

        print(current_page,total_page) 
        data['users'] = current_page
        data['total'] = total_page
        data['page_num'] = int(page)
        
        #渲染到前端
        return render_to_response(request,self.TEMPLATE,data=data)

class UpdateAdminStatus(View):

    def get(self,request):

        status = request.GET.get('status','on')

        print('status',status)
        _status = True if status == 'on' else False #True False 的if判断
        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manager'))
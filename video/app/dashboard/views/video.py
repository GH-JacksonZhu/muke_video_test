# coding:utf8

from app.libs.common import check_and_get_type
from django.views.generic import View
from django.shortcuts import redirect,reverse
from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from app.model.video import Video,VideoType,FromType,NationalityType,VideoSub as Video_Sub,IdentityType,VideoStar as Video_Star
class ExternaVideo(View):
    TEMPLATE = 'dashboard/video/externa_video.html'

    @dashboard_auth
    def get(self,request):
        data = {}
    
        error = request.GET.get('error','')
        data['error']=error

        videos=Video.objects.exclude(from_to=FromType.custom.value)
        data['videos'] = videos

        return render_to_response(request,self.TEMPLATE,data)

    def post(self,request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')

        if not all([name,image,video_type,from_to,nationality,info]):
            return redirect(f"{reverse('externa_video')}?error={'缺少必要信息'}")

        result = check_and_get_type(VideoType,video_type,'非法视频类型')
        if result.get('code') != 0:
            return redirect(f"{reverse('externa_video')}?error={result['msg']}")
        

        result = check_and_get_type(FromType,from_to,'非法视频来源')
        if result['code'] != 0:
            return redirect(f"{reverse('externa_video')}?error={result['msg']}")
        

        result = check_and_get_type(NationalityType,nationality,'非法制片地区')
        if result['code'] != 0:
            return redirect(f"{reverse('externa_video')}?error={result['msg']}")
        

        Video.objects.create(
            name=name,
            image=image,
            video_type=video_type,
            from_to=from_to,
            nationality = nationality,
            info=info
        )
        return redirect(reverse('externa_video'))

class VideoSub(View):
    TEMPLATE = 'dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self,request,video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        data['video']=video
        url_error = request.GET.get('url_error','')
        error = request.GET.get('error','')
        data['url_error'] = url_error
        data['error'] = error
        return render_to_response(request,self.TEMPLATE,data)

    def post(self,request,video_id):
        
        url = request.POST.get('url')
        video = Video.objects.get(pk=video_id)

        length = video.video_sub.count()

        existsed = video.video_sub.filter(url=url).exists()

        if existsed:
            return redirect(f"{reverse('video_sub',kwargs={'video_id':video_id})}?url_error={'地址已存在'}")
        else:
            Video_Sub.objects.create(video=video,url=url,number=length+int(1))

        return redirect(reverse('video_sub',kwargs={"video_id":video_id}))

class VideoStar(View):

    def post(self,request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')
        print(video_id)
        if not all([name,identity,video_id]):
            return redirect(f"{reverse('video_sub',kwargs={'video_id':video_id})}?error={'缺少必要字段'}")
        
        result = check_and_get_type(IdentityType,identity,"非法的身份")
        if result.get('code') != 0:
            return redirect(f"{reverse('video_sub',kwargs={'video_id':video_id})}?error={result['msg']}")

        video = Video.objects.get(pk=video_id)

        try:
            Video_Star.objects.create(
                video=video,
                name=name,
                identity=identity,
            )
        except:
            return redirect(f"{reverse('video_sub',kwargs={'video_id':video_id})}?error={'创建失败'}")
        
        return redirect(reverse('video_sub',kwargs={"video_id":video_id}))


class StatDelete(View):
    def get(self,request,star_id,video_id):

        Video_Star.objects.filter(id=star_id).delete()
    
        return redirect(reverse('video_sub',kwargs={"video_id":video_id}))
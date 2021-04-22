# coding:utf8

from django.urls import path
from .views.base import Index
from .views.auth import Login,Logout,AdminManager,UpdateAdminStatus
from .views.video import ExternaVideo, VideoSub, VideoStar, StatDelete

urlpatterns = [
    path('',Index.as_view(), name='dashboard_index'),
    path('login',Login.as_view(),name='dashboard_login'),
    path('logout',Logout.as_view(),name='dashboard_logout'),
    path('admin/manager',AdminManager.as_view(),name='admin_manager'),
    path('admin/manager/update/status',UpdateAdminStatus.as_view(),name='admin_update_status'),
    path('video/externa',ExternaVideo.as_view(),name='externa_video'),
    path('video/videosub/<int:video_id>',VideoSub.as_view(),name='video_sub'),
    path('video/videostar',VideoStar.as_view(),name='video_star'),
    path('video/videostar/delete/<int:star_id>/<int:video_id>',StatDelete.as_view(),name="star_delete")
]

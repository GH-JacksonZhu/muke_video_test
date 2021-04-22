#coding:utf8

from enum import Enum
from django.db import models

class VideoType(Enum):
    movie = 'movie'  #可以使用VideoType.movie.value获取
    cartoon = 'cartoon'
    episode = 'episode'
    variety = 'variety'
    other = 'other'

VideoType.movie.label = '电影'
VideoType.cartoon.label = '动漫'
VideoType.episode.label = '剧集'
VideoType.variety.label = '综艺'
VideoType.other.label = '其他'

class FromType(Enum):
    youku = 'youku'
    custom = 'custom'

FromType.youku.label = '优酷'
FromType.custom.label = '自制'

class NationalityType(Enum):
    china = 'china'
    japan = 'japan'
    korea = 'korea'
    america = 'america'
    other = 'other'

NationalityType.china.label = '中国'
NationalityType.japan.label = '日本'
NationalityType.america.label = '韩国'
NationalityType.korea.label = '美国'
NationalityType.other.label = '其他'

class IdentityType(Enum):
    to_star = "to_star"
    co_star = "co_star"
    director = "director"

IdentityType.to_star.label = '主演'
IdentityType.co_star.label = '配角'
IdentityType.director.label = '导演'


#电影信息
class Video(models.Model):
    name = models.CharField(max_length=100,null=False) #名称
    image = models.CharField(max_length=500,default='') #图片
    video_type = models.CharField(max_length=50,default=VideoType.other.value) #类型
    from_to = models.CharField(max_length=20,default=FromType.custom.value) #资源的源头
    nationality = models.CharField(max_length=20,default=NationalityType.other.value) #那个国家的
    info = models.TextField() #电影的详情
    status = models.BooleanField(default=True,db_index=True) #电影的状态
    created_time = models.DateTimeField(auto_now_add=True) 
    update_time = models.DateTimeField(auto_now=True)

    class Meta: #做联合索引
        unique_together = ('name','video_type','from_to','nationality')

    def __str__(self):
        return self.name

#电影演员信息
class VideoStar(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_star',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=100,null=False)
    identity = models.CharField(max_length=50,default='') #演员身份

    class Meta:
        unique_together = ('video','name','identity')
    
    def __str__(self):
        return self.name

#电影的播放地址
class VideoSub(models.Model):
    video = models.ForeignKey(
        Video,
        related_name='video_sub',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    url = models.CharField(max_length=500,null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ('video','number')
    
    def __str__(self):
        return f'video:{self.video.name},number:{self.number}'

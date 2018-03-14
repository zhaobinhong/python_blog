# -*- coding: utf-8 -*-

"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django.contrib.auth.views
from django.conf.urls import url, include
from django.contrib import admin

from article import views
from article.views import RSSFeed

urlpatterns = [

    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^(?P<id>\d+)/$', views.detail, name='detail'),
    url(r'^test/$', views.test, name='test'),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^about_me/$', views.about_me, name='about_me'),
    url(r'^tag(?P<tag>\w+)/$', views.search_tag, name='search_tag'),
    url(r'^search/$', views.blog_search, name='blog_search'),
    url(r'^feed/$', RSSFeed(), name="RSS"),

    url(r'^write/$', views.write, name="write"),
    url(r'^file/$', views.mgmt_files, name="file"),
    url(r'^shua/$', views.mgmt_file_download, name="download"),
    url(r'^download/$', views.download, name="download"),
    url(r'^rm/$', views.rm, name="rm"),

    url(r'^post/new/$', views.post_new, name="post_new"),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^accounts/(?P<pk>[0-9]+)/del/$', views.post_del, name='post_del'),

    url(r'^accounts/login/$', django.contrib.auth.views.login, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.logout, name='logout'),

    # url(r'^writeSql/$', views.writeSqlViewSet, name="writeSql"),

]

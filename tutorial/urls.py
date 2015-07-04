"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from tutorial.quickstart import viewss
from tutorial.quickstart.views import adminViews
from tutorial.quickstart.views import usersViews, wavsViews

router = routers.DefaultRouter()
router.register(r'users', viewss.UserViewSet)
router.register(r'groups', viewss.GroupViewSet)
router.register(r'Admins', adminViews.AdminViewSet)

router.register(r'Users', usersViews.UsersViewsSet)
router.register(r'Wavs', wavsViews.WavsViews)
#router.register(r'snippets/$', views.snippet_list)
#router.register(r'snippets/(?P<pk>[0-9]+)/$', views.snippet_detail)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [

    url(r'^snippets/$', viewss.snippet_list),
    url(r'^snippets/(?P<pk>[0-9]+)/$', viewss.snippet_detail),
    # url(r'Users/$', viewss.Users_list),
    url(r'admin/$', viewss.Admin_list),

]
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]



urlpatterns += [
    url(r'^index', viewss.index),
    url(r'^login', viewss.login),
    url(r'^logout', viewss.logout),
    url(r'^main', viewss.main),
    # user
    url(r'^user', viewss.user),
    url(r'^update',viewss.update),
    url(r'^add', viewss.add),
    url(r'^delete', viewss.delete),
    url(r'^search', viewss.search),
    url(r'^get', viewss.getUserById),


]
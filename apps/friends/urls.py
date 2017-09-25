from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'process$', views.process),
    url(r'friends$', views.success),
    url(r'success$', views.success),
    url(r'login$', views.login),
    url(r'add/(?P<friend_id>\d+)$', views.add),
    url(r'user/(?P<friend_id>\d+)$', views.user),
    url(r'remove/(?P<friend_id>\d+)$', views.remove),

]

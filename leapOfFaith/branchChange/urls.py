from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_request/$', views.login_request, name='login_request'),
    url(r'^register_request/$',
        views.register_request,
        name='register_request'),
    url(r'^(?P<roll_no>[0-9A-D]+)/$', views.profile, name='profile'),
    url(r'^(?P<roll_no>[0-9A-Da-z]+)/change$',
        views.update_pref,
        name='enter_preferences'),
    url(r'^(?P<roll_no>[0-9A-Da-z]+)/save$', views.save, name='save'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^Upload/$', views.Upload, name='Upload'),
    url(r'^download/$', views.download, name='download'),
    url(r'^idownload/$', views.idownload, name='idownload'),
    url(r'^(?P<roll_no>[0-9A-Da-z]+)/logout$', views.log_out, name='logout'),
]

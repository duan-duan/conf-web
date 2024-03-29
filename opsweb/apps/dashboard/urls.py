from django.conf.urls import include, url
from dashboard import users, role, power,views
app_name = 'dashboard'
urlpatterns = [
    url(r'^userlist/$', users.UserListView.as_view(), name='user_list'),
    url(r'^userdetail/(?P<pk>[0-9]+)?/$', users.UserDetailView.as_view(), name='user_detail'),
    url(r'^modifypasswd/$', users.ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^usergrouppower/(?P<pk>[0-9]+)?/$', users.UserGroupPowerView.as_view(), name='user_group_power'),

    url(r'^grouplist/$', role.GroupListView.as_view(), name='role_list'),
    url(r'^groupdetail/(?P<pk>[0-9]+)?/$', role.GroupDetailView.as_view(), name='role_detail'),
    url(r'^groupusers/$', role.GroupUsersView.as_view(), name='role_users'),


    url(r'^powerlist/$', power.PowerListView.as_view(), name='power_list'),
    url(r'^powerdetail/(?P<pk>[0-9]+)?/$', power.PowerDetailView.as_view(), name='power_detail'),
    url(r'^test_list/$', views.TestView.as_view(), name='test_list'),

]

from django.urls import path
from . import views

urlpatterns = [
    path('login_for_medal/', views.login_for_medal, name='login_for_medal'),
    path('login/',views.user_login,name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.user_logout,name='logout'),
    path('user_info/',views.user_info,name='user_info'),    # 个人资料
    path('change_nickname/',views.change_nickname,name='change_nickname'), # 修改用户昵称
    path('bind_email/',views.bind_email,name='bind_email'),                # 绑定邮箱
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'), # 发送验证码
    path('change_password/', views.change_password, name='change_password'),  # 修改密码
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # 忘记密码重置密码
]

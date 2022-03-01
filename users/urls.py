from django.urls import path
from users import views
urlpatterns = [
    path('accounts/kakao/login/', views.kakao_login, name='kakao_login'),
    path('accounts/kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('accounts/kakao/login/finish/', views.KakaoLogin.as_view(), name='kakao_login_todjango'),
    
]
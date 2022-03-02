from django.urls import path
from .views import KakaoSignIn


urlpatterns = [
    path('kakao/login/', KakaoSignIn.as_view()),
    
]
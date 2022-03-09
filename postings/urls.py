from django.urls import path, include
from .views import PostSearchView

urlpatterns = [
    path('search/', PostSearchView.as_view())
]

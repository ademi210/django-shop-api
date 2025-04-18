from . import views
from django.urls import path


urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('confirm/', views.SMSCodeConfirm.as_view()),
]
from django.urls import path

from forms import views

urlpatterns = [
    path('', views.FormList.as_view()),
    path('call/', views.call),
    path('calls/<int:pk>/', views.UpdateCall.as_view()),
]

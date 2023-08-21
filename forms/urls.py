from django.urls import path

from forms import views

urlpatterns = [
    path('', views.FormList.as_view()),
    path('next_time_slot/', views.GetNextTimeSlot.as_view()),
    path('calls/<int:pk>/', views.UpdateCall.as_view()),
]

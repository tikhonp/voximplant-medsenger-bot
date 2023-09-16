from django.urls import path

from forms_ai import views

urlpatterns = [
    path('calls/<int:pk>/request/', views.CallRequest.as_view()),
]

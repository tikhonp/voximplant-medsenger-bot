from django.urls import path

from medsenger_agent import views

urlpatterns = [
    path('init', views.InitAPIView.as_view()),
    path('remove', views.RemoveContractAPIView.as_view()),
    path('status', views.StatusAPIView.as_view()),
    path('settings', views.settings),

    path('settings/contract/', views.ContractDetail.as_view()),
    path('settings/time_slots/', views.SettingsTimeSlotsUpdate.as_view()),
    path('settings/forms/', views.SettingsFormsUpdate.as_view()),

]

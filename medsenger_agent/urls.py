from django.urls import path

from medsenger_agent import views

urlpatterns = [

    # Medsenger Agent urls
    path('init', views.MedsengerAgentInitView.as_view()),
    path('remove', views.MedsengerAgentRemoveContractView.as_view()),
    path('status', views.MedsengerAgentStatusView.as_view()),
    path('order', views.MedsengerAgentOrderView.as_view()),
    path('settings', views.MedsengerAgentSettingsView.as_view()),
    path('doctor_options', views.MedsengerAgentSettingsView.as_view()),  # For medsenger button

    # Settings page urls
    path('settings/contract/', views.ContractView.as_view()),
    path('settings/contract/time_slots/', views.ContractTimeSlotsView.as_view()),
    path('settings/contract/time_slots/<int:pk>/', views.ContractTimeSlotDetailView.as_view()),
    path('settings/contract/forms/', views.ContractFormsView.as_view()),
    path('settings/contract/forms/<int:pk>/', views.ContractFormDetailView.as_view()),
    path('settings/contract/calls/', views.ContractCallsView.as_view()),

]

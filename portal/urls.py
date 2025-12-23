from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='user-home'),

    path('request/new/', views.create_request_view, name='new-request'),

    path('update-status/<int:pk>/<str:new_status>/', views.update_status_view, name='update-status'),

    path('delete-request/<int:pk>/', views.delete_request_view, name='delete-request'),

    path('request-details/<int:pk>/', views.request_details_view, name='request-details'),
]
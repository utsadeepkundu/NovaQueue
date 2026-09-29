from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup_patient, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='public/login.html'), name='login'),
    
    path('dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('login-success/', views.login_success, name='login_success'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    path('request-token/', views.request_token, name='request_token'),

    path('admin-dashboard/queue/', views.manage_queue, name='manage_queue'),
    path('admin-dashboard/queue/call-next/', views.call_next_patient, name='call_next_patient'),
    path('admin-dashboard/queue/update/<int:pk>/<str:new_status>/', views.update_queue_status, name='update_status'),

    path('profile/settings/', views.profile_settings, name='profile_settings'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/queue/complete/<int:pk>/', views.complete_session, name='complete_session'),
    path('my-tokens/', views.my_tokens, name='my_tokens'),
    path('history/', views.patient_history, name='patient_history'),   
    path('admin-dashboard/history/', views.admin_history, name='admin_history'),
    
    path('admin-dashboard/history/edit/<int:pk>/', views.history_edit, name='history_edit'),
    path('admin-dashboard/history/delete/<int:pk>/', views.history_delete, name='history_delete'),
    path('admin-dashboard/scanner/', views.qr_scanner, name='qr_scanner'),
    path('api/check-in/', views.process_check_in, name='process_check_in'),
    path('admin-dashboard/patients/', views.patient_list, name='manage_patients'),
    path('admin-dashboard/patients/add/', views.patient_create, name='add_patient'),
    path('admin-dashboard/patients/edit/<int:pk>/', views.patient_update, name='edit_patient'),
    path('admin-dashboard/patients/delete/<int:pk>/', views.patient_delete, name='delete_patient'),

    # Patient Routes
    path('appointments/book/', views.book_appointment, name='book_appointment'),
    path('appointments/my/', views.my_appointments, name='my_appointments'),
    path('admin-dashboard/analytics/', views.admin_analytics, name='admin_analytics'),
    # Admin Routes
    path('admin-dashboard/queue/walkin/', views.generate_offline_token, name='generate_offline_token'),
    path('admin-dashboard/appointments/', views.admin_appointments, name='admin_appointments'),
    path('admin-dashboard/appointments/complete/<int:pk>/', views.complete_appointment, name='complete_appointment'),
]
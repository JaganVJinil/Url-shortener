from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('', views.url_list, name='url_list'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_url, name='add_url'),
    path('edit/<int:pk>/', views.edit_url, name='edit_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('<str:short_code>/', views.redirect_short_url, name='redirect_short_url'), 
    path('accounts/login/', views.login_view),
]

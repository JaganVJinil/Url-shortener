from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),                     # login at root
    path('signup/', views.signup_view, name='signup'),
    path('urllist/', views.url_list, name='url_list'),            # url_list moved
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_url, name='add_url'),
    path('edit/<int:pk>/', views.edit_url, name='edit_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('<str:short_code>/', views.redirect_short_url, name='redirect_short_url'),
    path('accounts/login/', views.login_view),
]

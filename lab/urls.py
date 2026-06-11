from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # SQL Injection
    path('sqli/login/', views.sqli_login, name='sqli_login'),
    path('sqli/search/', views.sqli_search, name='sqli_search'),
    path('sqli/product/', views.sqli_product, name='sqli_product'),

    # XSS
    path('xss/reflected/', views.xss_reflected, name='xss_reflected'),
    path('xss/stored/', views.xss_stored, name='xss_stored'),
    path('xss/stored/<int:post_id>/', views.xss_stored, name='xss_stored'),
    path('xss/dom/', views.xss_dom, name='xss_dom'),

    # File Upload
    path('upload/', views.upload_file, name='upload_file'),

    # Command Injection
    path('cmd/', views.cmd_injection, name='cmd_injection'),

    # Path Traversal
    path('file/', views.path_traversal, name='path_traversal'),

    # IDOR
    path('profile/<int:user_id>/', views.idor_profile, name='idor_profile'),
    path('profile/<int:user_id>/update-email/', views.idor_update_email, name='idor_update_email'),

    # Open Redirect
    path('redirect/', views.open_redirect, name='open_redirect'),

    # CSRF
    path('transfer/', views.csrf_transfer, name='csrf_transfer'),

    # Info disclosure
    path('feedback/', views.feedback, name='feedback'),
    path('debug/', views.debug_info, name='debug_info'),
    path('robots.txt', views.robots, name='robots'),
    path('.well-known/security.txt', views.security_txt, name='security_txt'),
]

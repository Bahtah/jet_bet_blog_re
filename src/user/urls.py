from django.urls import path
from . import views

urlpatterns = [
    path('173e0222ccfb6c76e92fb8df9a19b645da151fa3d6b1d158262e26aa6bdff4ed/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

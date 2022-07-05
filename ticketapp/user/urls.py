from . import views
from django.urls import path
urlpatterns = [
    path('login/', views.loginView, name="login"),
    path('logout/', views.logoutView, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('emailVerification/<uidb64>/<token>',
         views.activate, name='emailActivate')

]

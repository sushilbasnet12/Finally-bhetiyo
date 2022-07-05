from . import views
from django.urls import path
urlpatterns = [
    path('', views.index, name="allmatches"),
    path('<int:id>/', views.match),
    path('<int:id>/reserve', views.reserve)
    # path('logout/', views.logoutView, name="logout"),
    # path('register/', views.registerPage, name="register")
]

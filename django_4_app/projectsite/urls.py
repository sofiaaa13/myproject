from django.urls import path
from . import views
urlpatterns = [
    path('profile/<int:id>/', views.ProfilePage.as_view()),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration')
]

from django.urls import path
from user import views

urlpatterns = [
    path('teachers/', views.TeacherView.as_view(), name='teachers'),

    # authentication users
    path('register-page/', views.RegisterUserView.as_view(), name='register'),
    path('login-page/', views.LoginUserView.as_view(), name='login'),
    path('logout-page/', views.LogoutView.as_view(), name='logout'),
    path('forgotten-password/', views.forgot_password, name='forgotten_password'),

    # Profile
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),

    # Activation
    path('activation-link/<uidb64>/<token>/', views.AccountActivationView.as_view(), name='activate')

]

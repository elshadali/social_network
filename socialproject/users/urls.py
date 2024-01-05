from django.urls import path
from .views import user_login, user_logout, index, register, edit
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('', index, name='index'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'), name='password_change'
        ),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'
        ),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'
        ),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'
        ),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'
        ),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'
        ),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
    

]


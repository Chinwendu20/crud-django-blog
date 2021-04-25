
from .views import BlogCreateView, BlogDetailView, BlogListView, BlogUpdateView, BlogDeleteView, signup, comments
from django.urls import path 
from django.contrib.auth import views as auth_views


urlpatterns = [
		
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
        name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
        name='password_change_done'),
		path('signup/', signup, name='signup'),
		path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
		path('logout/', auth_views.LogoutView.as_view(), name='logout'),
		path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),
		path('post/<int:pk>/edit/', BlogUpdateView.as_view(), name='post_edit'),
		path('post/<int:pk>/reply/', comments, name='reply'),
		path('post/new/', BlogCreateView.as_view(), name='post_new'),
		path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
		path('', BlogListView.as_view(), name='home')
]


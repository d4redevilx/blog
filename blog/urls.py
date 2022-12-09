from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signout/', views.signout, name='signout'),
    path('posts/new', views.CreatePostView.as_view(), name='new_post'),
    path('posts/<int:id_post>', views.PostView.as_view(), name='post'),
    path('posts/<int:id_post>/edit',
         views.PostEditView.as_view(), name='post_edit'),
    path('posts/<int:id_post>/delete',
         views.PostDeleteView.as_view(), name='post_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

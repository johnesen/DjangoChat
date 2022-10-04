from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from users import views as users_views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs', include_docs_urls(title='NJohnny')),
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path('product/', include('product.urls')),
    path('login/', users_views.LoginAPIView.as_view(), name='login'),
    path('register/', users_views.RegisterAPIView.as_view(), name='register'),
    path('v1/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

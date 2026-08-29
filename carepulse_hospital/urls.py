from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)
from drf_spectacular.views import (SpectacularAPIView,SpectacularSwaggerView,)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),

    # JWT
    path('api/auth/token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('api/auth/token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
    # API Documentation
    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui' ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
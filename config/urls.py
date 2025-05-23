from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.response import Response

from config import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Task management system API",
        default_version='v1',
        description="task management system",
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


def task_view(request):
    return Response({"salom": "salom"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include(
        [
            path('', task_view),

            path('task_manager/', include('task_manager.urls')),
            path('accounts/', include('accounts.urls')),
            path('notifications/', include('notifications.urls')),
        ]
    )),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

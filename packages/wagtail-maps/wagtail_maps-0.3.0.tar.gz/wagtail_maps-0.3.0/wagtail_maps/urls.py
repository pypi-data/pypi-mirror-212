from django.urls import include, path

from .api import views as api_views

app_name = 'wagtail_maps'

api_patterns = [
    path('<int:pk>/', api_views.map_detail, name='map-detail'),
]

urlpatterns = [
    path('api/v1/', include((api_patterns, 'api'))),
]

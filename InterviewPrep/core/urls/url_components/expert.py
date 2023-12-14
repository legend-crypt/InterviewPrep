from django.urls import path
from core.views.expert import ExpertViewSet

urlpatterns = [
    path('experts/', ExpertViewSet.as_view({'get': 'list'})),
    path('experts/<uuid:pk>/', ExpertViewSet.as_view({'get': 'retrieve'})),
    path('experts/create/', ExpertViewSet.as_view({'post': 'create'})),
    path('experts/update-form/<uuid:pk>/', ExpertViewSet.as_view({'post': 'update'})),
]

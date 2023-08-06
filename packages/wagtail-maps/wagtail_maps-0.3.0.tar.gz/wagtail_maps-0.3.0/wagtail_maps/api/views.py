from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ..models import Map
from .serializers import MapSerializer


class MapsAPIViewSet(RetrieveModelMixin, GenericViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


map_detail = MapsAPIViewSet.as_view({'get': 'retrieve'})

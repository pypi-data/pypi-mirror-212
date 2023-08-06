from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import CiscoSupportSerializer, CiscoDeviceTypeSupportSerializer


class CiscoSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoSupport.objects.prefetch_related("tags")
    serializer_class = CiscoSupportSerializer


class CiscoDeviceTypeSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceTypeSupport.objects.prefetch_related("tags")
    serializer_class = CiscoDeviceTypeSupportSerializer

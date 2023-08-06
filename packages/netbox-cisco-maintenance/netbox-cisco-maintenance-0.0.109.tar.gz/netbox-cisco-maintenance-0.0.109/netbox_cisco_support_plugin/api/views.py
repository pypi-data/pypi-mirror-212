from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import CiscoSupportSerializer, CiscoDeviceTypeSupportSerializer


class CiscoSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoSupport.objects.all().prefetch_related("device_type_support")
    serializer_class = CiscoSupportSerializer


class CiscoDeviceTypeSupportViewSet(NetBoxModelViewSet):
    queryset = models.CiscoDeviceTypeSupport.objects.all()
    serializer_class = CiscoDeviceTypeSupportSerializer

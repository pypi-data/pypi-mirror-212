from netbox.api.viewsets import NetBoxModelViewSet

from .. import models
from . import serializers


class LDP_ViewSet(NetBoxModelViewSet):
    queryset = models.LDP.objects.all()
    serializer_class = serializers.LDPSerializer


class BGP_CE_ViewSet(NetBoxModelViewSet):
    queryset = models.BGP_CE.objects.all()
    serializer_class = serializers.BGP_CESerializer


class BGP_PE_ViewSet(NetBoxModelViewSet):
    queryset = models.BGP_PE.objects.all()
    serializer_class = serializers.BGP_PESerializer


class BGP_Mesh_ViewSet(NetBoxModelViewSet):
    queryset = models.BGP_Mesh.objects.all()
    serializer_class = serializers.BGP_MeshSerializer


class Address_Family_ViewSet(NetBoxModelViewSet):
    queryset = models.Address_Family.objects.all()
    serializer_class = serializers.Address_FamilySerializer


class MPLS_Instance_ViewSet(NetBoxModelViewSet):
    queryset = models.MPLS_Instance.objects.all()
    serializer_class = serializers.MPLS_InstanceSerializer

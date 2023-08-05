from extras.api.serializers import CustomFieldSerializer
from netbox.api.serializers.base import ValidatedModelSerializer
from rest_framework import serializers

from netbox.api.serializers import WritableNestedSerializer
from .. import models

from .. import config


class BaseModelSerializer(CustomFieldSerializer, ValidatedModelSerializer):
    """
    Adds support for custom fields and tags.
    """

    pass


class NestedLDPSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:ldp')

    class Meta:
        model = models.LDP
        fields = (
            'id',
            'url',
            'device',
            'label_start',
            'label_end',
            'auto_range',
            'last_updated',
        )


class LDPSerializer(BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:ldp')

    class Meta:
        model = models.LDP
        fields = (
            'id',
            'display',
            'custom_fields',  # From BaseModelSerializer
            'created',
            'last_updated',  # From NetBoxModel
            'url',  # From RouteTargetSerializer
            'device',
            'label_start',
            'label_end',
            'auto_range',
            'comments',  # From LDP
        )


class Nested_BGP_CESerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:bgp_ce')

    class Meta:
        model = models.BGP_CE
        fields = (
            'id',
            'url',
            'name',
            'ip_addresses',
            'asn',
            'comments',
            'last_updated',
        )


class BGP_CESerializer(BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:bgp_ce')

    class Meta:
        model = models.BGP_CE
        fields = (
            'id',
            'display',
            'custom_fields',  # From BaseModelSerializer
            'created',
            'last_updated',  # From NetBoxModel
            'url',  # From RouteTargetSerializer
            'name',  # From BGP_CE
            'ip_addresses',
            'asn',
            'comments',
        )


class Nested_BGP_PESerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:bgp_pe')

    class Meta:
        model = models.BGP_PE
        fields = (
            'id',
            'url',
            'device',
            'update_source_interface',
            'asn',
            'advertised_customers',
            'comments',
            'last_updated',
        )


class BGP_PESerializer(BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:bgp_pe')

    class Meta:
        model = models.BGP_PE
        fields = (
            'id',
            'display',
            'custom_fields',  # From BaseModelSerializer
            'created',
            'last_updated',  # From NetBoxModel
            'url',  # From RouteTargetSerializer
            'device',  # From BGP_PE
            'update_source_interface',
            'asn',
            'advertised_customers',
            'comments',
        )


class Nested_BGP_MeshSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:bgp_mesh')

    class Meta:
        model = models.BGP_Mesh
        fields = (
            'id',
            'url',
            'name',
            'bgp_mesh',
            'comments',
            'last_updated',
        )


class BGP_MeshSerializer(BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:bgp_mesh')

    class Meta:
        model = models.BGP_Mesh
        fields = (
            'id',
            'display',
            'custom_fields',  # From BaseModelSerializer
            'created',
            'last_updated',  # From NetBoxModel
            'url',  # From RouteTargetSerializer
            'bgp_mesh',  # From BGP_Mesh
            'name',
            'comments',
        )


class Nested_Address_Family_Serializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:address_family')

    class Meta:
        model = models.Address_Family
        fields = (
            'id',
            'url',
            'name',
            'vpnv4_address_family',
            'vpnv4_community',
            'vpnv6_address_family',
            'vpnv6_community',
            'comments',
            'last_updated',
        )


class Address_FamilySerializer(BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:address_family')

    class Meta:
        model = models.Address_Family
        fields = (
            'id',
            'display',
            'custom_fields',  # From BaseModelSerializer
            'created',
            'last_updated',  # From NetBoxModel
            'url',  # From RouteTargetSerializer
            'name',  # From BGP_Mesh
            'vpnv4_address_family',
            'vpnv4_community',
            'vpnv6_address_family',
            'vpnv6_community',
            'comments',
        )


class Nested_MPLS_Instance_Serializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:mpls_instance')

    class Meta:
        model = models.MPLS_Instance
        fields = (
            'id',
            'url',
            'ibgp',
            'service',
            'name',
            'comments',
            'last_updated',
        )


class MPLS_InstanceSerializer(BaseModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name=f'plugins:{config.name}:mpls_instance')

    class Meta:
        model = models.MPLS_Instance
        fields = (
            'id',
            'display',
            'custom_fields',  # From BaseModelSerializer
            'created',
            'last_updated',  # From NetBoxModel
            'url',  # From RouteTargetSerializer
            'ibgp',  # From BGP_Mesh
            'service',
            'name',
            'comments',
        )

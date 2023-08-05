from graphene import ObjectType, Field, ResolveInfo
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import models


#
# Object types
#


class LDP_Type(NetBoxObjectType):
    class Meta:
        model = models.LDP
        fields = '__all__'


class BGP_CE_Type(NetBoxObjectType):
    class Meta:
        model = models.BGP_CE
        fields = '__all__'


class BGP_PE_Type(NetBoxObjectType):
    class Meta:
        model = models.BGP_PE
        fields = '__all__'

    bgp_mesh = Field(lambda: BGP_Mesh_Type)

    def resolve_bgp_mesh(root: 'BGP_PE_Type', info: ResolveInfo):
        bgp_meshes = root.bgp_mesh.all()
        if bgp_meshes:
            return bgp_meshes.first()
        return None


class BGP_Mesh_Type(NetBoxObjectType):
    class Meta:
        model = models.BGP_Mesh
        fields = '__all__'


class Address_Family_Type(NetBoxObjectType):
    class Meta:
        model = models.Address_Family
        fields = '__all__'


class MPLS_Instance_Type(NetBoxObjectType):
    class Meta:
        model = models.MPLS_Instance
        fields = '__all__'


#
# Queries
#


class Query(ObjectType):
    ldp = ObjectField(LDP_Type)
    ldp_list = ObjectListField(LDP_Type)

    bgp_ce = ObjectField(BGP_CE_Type)
    bgp_ce_list = ObjectListField(BGP_CE_Type)

    bgp_pe = ObjectField(BGP_PE_Type)
    bgp_pe_list = ObjectListField(BGP_PE_Type)

    bgp_mesh = ObjectField(BGP_Mesh_Type)
    bgp_mesh_list = ObjectListField(BGP_Mesh_Type)

    address_family = ObjectField(Address_Family_Type)
    address_family_list = ObjectListField(Address_Family_Type)

    mpls_instance = ObjectField(MPLS_Instance_Type)
    mpls_instance_list = ObjectListField(MPLS_Instance_Type)


schema = Query

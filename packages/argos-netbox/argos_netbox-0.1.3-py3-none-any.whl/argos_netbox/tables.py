import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from . import models, config

# List of entries


class LDP_Table(NetBoxTable):
    device = tables.Column(
        linkify=True,
    )

    range = tables.Column()

    class Meta(NetBoxTable.Meta):
        model = models.LDP
        fields = ('id', 'device', 'range', 'ldp_enabled_interfaces', 'last_updated')
        default_columns = ('id', 'device', 'range', 'ldp_enabled_interfaces')

    def render_ldp_enabled_interfaces(self, record):
        interfaces = record.ldp_enabled_interfaces.all()
        interface_links = []
        for interface in interfaces:
            url = reverse('dcim:interface', kwargs={'pk': interface.pk})
            interface_links.append(format_html('<a href="{}">{}</a>', url, interface))
        return format_html(', '.join(interface_links))


class BGP_CE_Table(NetBoxTable):
    asn = tables.Column(
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = models.BGP_CE
        fields = ('id', 'name', 'asn', 'last_updated')
        default_columns = ('id', 'name', 'asn')


class BGP_PE_Table(NetBoxTable):
    device = tables.Column(
        linkify=True,
    )
    update_source_interface = tables.Column(
        linkify=True,
    )
    asn = tables.Column(
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = models.BGP_PE
        fields = ('id', 'device', 'update_source_interface', 'asn', 'advertised_customers', 'last_updated')
        default_columns = ('id', 'device', 'update_source_interface', 'asn', 'advertised_customers')

    def render_advertised_customers(self, record):
        customers = record.advertised_customers.all()
        customer_links = []
        for customer in customers:
            url = reverse(f'plugins:{config.name}:bgp_ce', kwargs={'pk': customer.pk})
            customer_links.append(format_html('<a href="{}">{}</a>', url, customer))
        return format_html(', '.join(customer_links))


class BGP_Mesh_Table(NetBoxTable):
    bgp_mesh = tables.ManyToManyColumn(
        linkify=True,
    )

    name = tables.Column(
        linkify=True,
    )

    address_family = tables.Column(
        linkify=True,
    )

    class Meta(NetBoxTable.Meta):
        model = models.BGP_Mesh
        fields = ('id', 'bgp_mesh', 'name', 'address_family' 'last_updated')
        default_columns = ('id', 'bgp_mesh', 'name', 'address_family')


class Address_Family_Table(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    vpnv4_community = ChoiceFieldColumn()

    vpnv6_community = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = models.Address_Family
        fields = ('id', 'name', 'vpnv4_community', 'vpnv6_community', 'last_updated')
        default_columns = ('id', 'name', 'vpnv4_community', 'vpnv6_community')


class MPLS_Instance_Table(NetBoxTable):
    name = tables.Column(
        linkify=True,
    )

    ibgp = tables.Column(
        linkify=True,
    )

    service = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = models.MPLS_Instance
        fields = ('id', 'name', 'ibgp', 'service', 'last_updated')
        default_columns = ('id', 'name', 'ibgp', 'service')

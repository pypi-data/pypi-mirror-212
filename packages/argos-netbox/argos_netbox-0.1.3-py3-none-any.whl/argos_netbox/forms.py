from typing import Dict

from dcim.models.device_components import Interface
from ipam.models.ip import IPAddress
from django.db.models import Q
from utilities.forms.fields import CommentField
from utilities.forms.fields import DynamicModelMultipleChoiceField
from utilities.forms.fields.dynamic import DynamicModelMultipleChoiceField, DynamicModelChoiceField

from netbox.forms import NetBoxModelForm

from . import models

# HTML rendering


class LDP_Form(NetBoxModelForm):
    """Form to fill out LDP instance."""

    comments = CommentField()

    ldp_enabled_interfaces = DynamicModelMultipleChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        label="LDP enabled interfaces",
        query_params={
            "device_id": "$device",
        },
    )

    class Meta:
        model = models.LDP
        fields = ('device', 'auto_range', 'ldp_enabled_interfaces', 'label_start', 'label_end', 'comments')

    def clean(self):
        data: Dict = super().clean()
        start = data.get('label_start')
        end = data.get('label_end')
        auto = data.get('auto_range')
        if not auto:
            if start is not None and end is not None:
                min_value, max_value = 0, 1048575
                if not (min_value <= int(start) <= max_value):
                    self.add_error('label_start', f"Label outside range: [{min_value};{max_value}]")
                if not (min_value <= int(end) <= max_value):
                    self.add_error('label_end', f"Label outside range: [{min_value};{max_value}]")
                if not (int(end) > int(start)):
                    msg = "Label end must exceed label start."
                    self.add_error('label_start', msg)
                    self.add_error('label_end', msg)
            else:
                if start is None:
                    self.add_error('label_start', f"Missing value.")
                if end is None:
                    self.add_error('label_end', f"Missing value.")
        return data


class BGP_CE_Form(NetBoxModelForm):
    """Form to fill out BGP CE instance."""

    comments = CommentField()

    class Meta:
        model = models.BGP_CE
        fields = ('name', 'ip_addresses', 'asn', 'comments')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ip_addresses'].choices = [
            (ip_address.pk, f"{ip_address.address}" + (f" - {ip_address.vrf}" if ip_address.vrf is not None else ""))
            for ip_address in IPAddress.objects.all()
        ]


class BGP_PE_Form(NetBoxModelForm):
    """Form to fill out BGP PE instance."""

    comments = CommentField()

    update_source_interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=True,
        label="Interface for BGP exchange",
        query_params={
            "device_id": "$device",
        },
    )

    class Meta:
        model = models.BGP_PE
        fields = (
            'device',
            'update_source_interface',
            'asn',
            'advertised_customers',
            'comments',
        )


class BGP_Mesh_Form(NetBoxModelForm):
    """Form to fill out BGP Mesh Neighbourhood instance."""

    comments = CommentField()

    bgp_mesh = DynamicModelMultipleChoiceField(
        queryset=models.BGP_PE.objects.all(),
        label="BGP PEs",
        help_text="Select BGP PE devices which are part of this mesh.",
        required=True,
    )

    class Meta:
        model = models.BGP_Mesh
        fields = (
            'name',
            'bgp_mesh',
            'address_family',
            'comments',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mesh: models.BGP_Mesh = kwargs['instance']
        queryset = models.BGP_PE.objects.filter(Q(bgp_mesh=None) | Q(bgp_mesh=mesh.pk))
        self.fields['bgp_mesh'].queryset = queryset


class Address_Family_Form(NetBoxModelForm):
    """Form to fill out Address Family instance."""

    comments = CommentField()

    class Meta:
        model = models.Address_Family
        fields = (
            'name',
            'vpnv4_address_family',
            'vpnv4_community',
            'vpnv6_address_family',
            'vpnv6_community',
            'comments',
        )


class MPLS_Instance_Form(NetBoxModelForm):
    """Form to fill out Address Family instance."""

    comments = CommentField()

    class Meta:
        model = models.MPLS_Instance
        fields = (
            'name',
            'ibgp',
            'service',
            'comments',
        )

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet

from . import config


class Community_Choices(ChoiceSet):
    key = 'Address_Family.action'

    CHOICES = [
        ('standard', 'Standard'),
        ('extended', 'Extended'),
        ('both', 'Both'),
    ]


class MPLS_Choices(ChoiceSet):
    key = 'MPLS_Instance.action'

    CHOICES = [
        ('mpls_l3_vpn', 'MPLS L3 VPN', 'blue'),
    ]


class LDP(NetBoxModel):
    """Single LDP range."""

    device = models.OneToOneField(
        blank=False,
        on_delete=models.deletion.PROTECT,
        to="dcim.device",
    )

    ldp_enabled_interfaces = models.ManyToManyField(
        to="dcim.interface",
        limit_choices_to=models.Q(device_id=models.F("device")),
        blank=False,
        verbose_name="LDP Interfaces",
    )

    auto_range = models.BooleanField(
        default=True,
        help_text="Whether the lable range should be determined by the device itself.",
    )

    label_start = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1048575)],
        help_text="Value between [0; 1048575]",
    )

    label_end = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1048575)],
        help_text="Value between [0; 1048575]",
    )

    comments = models.TextField()

    last_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'LDP Participant'
        verbose_name_plural = 'LDP Participants'

    def __str__(self) -> str:
        return f'{self.device}'

    @property
    def range(self):
        return "Auto" if self.auto_range else f"[{self.label_start}; {self.label_end}]"

    def get_absolute_url(self):
        return reverse(f"plugins:{config.name}:ldp", args=[self.pk])


class BGP_CE(NetBoxModel):
    """Single CE Device."""

    name = models.CharField(
        blank=False,
        max_length=50,
    )

    ip_addresses = models.ManyToManyField(
        to="ipam.ipaddress",
        blank=False,
        verbose_name="PE facing IP addresses",
    )

    asn = models.ForeignKey(
        to="ipam.asn",
        blank=False,
        verbose_name="ASN of CE device",
        on_delete=models.deletion.PROTECT,
    )

    comments = models.TextField()

    last_updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = 'BGP Customer Edge'
        verbose_name_plural = 'BGP Customer Edges'

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse(f"plugins:{config.name}:bgp_ce", args=[self.pk])


class BGP_PE(NetBoxModel):
    """Single PE device."""

    device = models.OneToOneField(
        blank=False,
        on_delete=models.deletion.PROTECT,
        to="dcim.device",
    )

    update_source_interface = models.OneToOneField(
        to="dcim.interface",
        limit_choices_to=models.Q(device_id=models.F("device")),
        on_delete=models.deletion.PROTECT,
        blank=False,
        verbose_name="Interfaces used for BGP exchange",
    )

    asn = models.ForeignKey(
        to="ipam.asn",
        blank=False,
        verbose_name="ASN",
        on_delete=models.deletion.PROTECT,
    )

    advertised_customers = models.ManyToManyField(
        to=BGP_CE,
        blank=True,
        verbose_name="Advertised CEs",
    )

    last_updated = models.DateTimeField(auto_now=True, null=True)

    comments = models.TextField()

    class Meta:
        verbose_name = 'BGP Provider Edge'
        verbose_name_plural = 'BGP Provider Edges'

    def __str__(self) -> str:
        return f'{self.device}'

    def get_absolute_url(self):
        return reverse(f"plugins:{config.name}:bgp_pe", args=[self.pk])


class Address_Family(NetBoxModel):
    """Address Family"""

    name = models.CharField(
        blank=False,
        max_length=50,
    )

    vpnv4_address_family = models.BooleanField(
        default=True,
        help_text="Whether the vpnv4-address-family should be active or not",
    )

    vpnv4_community = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=Community_Choices,
    )

    vpnv6_address_family = models.BooleanField(
        default=True,
        help_text="Whether the vpnv6-address-family should be active or not",
    )

    vpnv6_community = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=Community_Choices,
    )

    last_updated = models.DateTimeField(auto_now=True, null=True)

    comments = models.TextField()

    class Meta:
        verbose_name = 'Address Family'
        verbose_name_plural = 'Address Families'

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse(f"plugins:{config.name}:address_family", args=[self.pk])


class BGP_Mesh(NetBoxModel):
    """BGP Mesh Neighbourhood"""

    name = models.CharField(
        blank=False,
        max_length=50,
    )

    bgp_mesh = models.ManyToManyField(
        to=BGP_PE,
        blank=False,
        verbose_name="BGP PEs",
        related_name="bgp_mesh",
    )

    address_family = models.ForeignKey(
        to=Address_Family,
        blank=False,
        on_delete=models.deletion.PROTECT,
        verbose_name="Address Family",
    )

    last_updated = models.DateTimeField(auto_now=True, null=True)

    comments = models.TextField()

    class Meta:
        verbose_name = 'BGP Mesh'
        verbose_name_plural = 'BGP Meshes'

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse(f"plugins:{config.name}:bgp_mesh", args=[self.pk])


class MPLS_Instance(NetBoxModel):
    """BGP Mesh Neighbourhood"""

    name = models.CharField(
        blank=False,
        max_length=50,
    )

    ibgp = models.OneToOneField(
        to=BGP_Mesh,
        blank=False,
        on_delete=models.deletion.PROTECT,
        verbose_name="iBGP Network",
        related_name="ibgp",
    )

    service = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        choices=MPLS_Choices,
    )

    last_updated = models.DateTimeField(auto_now=True, null=True)

    comments = models.TextField()

    class Meta:
        verbose_name = 'MPLS Instance'
        verbose_name_plural = 'MPLS Instances'

    def __str__(self) -> str:
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse(f"plugins:{config.name}:mpls_instance", args=[self.pk])

    def get_service_color(self):
        return MPLS_Choices.colors.get(self.service)

from extras.plugins import PluginConfig
from .version import __version__


class ArgosPluginConfig(PluginConfig):
    name = 'argos_netbox'
    verbose_name = 'Argos'
    description = 'Manage simple MPLS in NetBox'
    version = __version__
    base_url = 'argos'
    min_version = '3.4.0'


config = ArgosPluginConfig

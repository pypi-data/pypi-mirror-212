from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

from . import config

#
# Sidebar nav content
#

menu_items = (
    PluginMenuItem(
        link=f'plugins:{config.name}:ldp_list',
        link_text='LDP',
        buttons=[
            PluginMenuButton(
                link=f'plugins:{config.name}:ldp_add',
                title='Add LDP Participant',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
            )
        ],
    ),
    PluginMenuItem(
        link=f'plugins:{config.name}:bgp_ce_list',
        link_text='BGP CE',
        buttons=[
            PluginMenuButton(
                link=f'plugins:{config.name}:bgp_ce_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
            )
        ],
    ),
    PluginMenuItem(
        link=f'plugins:{config.name}:bgp_pe_list',
        link_text='BGP PE',
        buttons=[
            PluginMenuButton(
                link=f'plugins:{config.name}:bgp_pe_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
            )
        ],
    ),
    PluginMenuItem(
        link=f'plugins:{config.name}:bgp_mesh_list',
        link_text='BGP Mesh',
        buttons=[
            PluginMenuButton(
                link=f'plugins:{config.name}:bgp_mesh_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
            )
        ],
    ),
    PluginMenuItem(
        link=f'plugins:{config.name}:address_family_list',
        link_text='Address Family',
        buttons=[
            PluginMenuButton(
                link=f'plugins:{config.name}:address_family_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
            )
        ],
    ),
    PluginMenuItem(
        link=f'plugins:{config.name}:mpls_instance_list',
        link_text='MPLS Instance',
        buttons=[
            PluginMenuButton(
                link=f'plugins:{config.name}:mpls_instance_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
            )
        ],
    ),
)

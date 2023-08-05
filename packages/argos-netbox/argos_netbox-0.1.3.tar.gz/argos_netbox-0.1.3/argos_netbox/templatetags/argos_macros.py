from django import template

register = template.Library()


@register.inclusion_tag('argos_netbox/util/hide_if_checked.html')
def hide_if_checked(checkbox_field_name, block_id, reverse=False):
    reverse = 1 if reverse else 0
    return {'checkbox_field_name': checkbox_field_name, 'block_id': block_id, 'reverse': reverse}

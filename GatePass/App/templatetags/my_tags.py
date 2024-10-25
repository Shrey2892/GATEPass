# myapp/templatetags/my_tags.py

from django import template
from django.urls import reverse

register = template.Library()

@register.simple_tag
def out_pass_success_url(gatepassno):
    """Generate URL for out_pass_success with the given gatepassno."""
    return reverse('out_pass_success', kwargs={'gatepassno': gatepassno})

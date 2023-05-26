from django import template
from django.urls import reverse

from home.models import Setting



register = template.Library()


@register.simple_tag
def settingstag():
    setting = Setting.objects.get(pk=1)
    return setting

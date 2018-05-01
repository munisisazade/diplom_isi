from django import template
from games.models import WebsiteHeader
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def count(var, t):
    return var[int(t)]


@register.filter
def duration_field(val):
    seconds = val.seconds
    minutes = seconds // 60
    seconds = seconds % 60
    minutes = minutes % 60
    return "{:02d}:{:02d}".format(minutes, seconds)


@register.assignment_tag
def get_data():
    try:
        obj = WebsiteHeader.objects.all().last()
        if obj:
            return obj
        else:
            return False
    except:
        return False


@register.filter
def getIndex(arr, elem):
    try:
        return arr.index(elem)
    except:
        return False

@register.filter
def get_uuid(social_obj):
    if social_obj:
        try:
            return social_obj.get(provider='facebook').uid
        except:
            return '100002461198950'
    else:
        return '100002461198950'

@register.filter("parse_duration")
def parse_duration(value):
    try:
        return str(timedelta(milliseconds=value))
    except:
        pass

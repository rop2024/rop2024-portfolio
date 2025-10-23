from django import template
import json

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter to get dictionary item by key"""
    return dictionary.get(key, 0)

@register.filter
def to_json(value):
    """Convert Python object to JSON string safely"""
    try:
        return json.dumps(value)
    except (TypeError, ValueError):
        return '{}'
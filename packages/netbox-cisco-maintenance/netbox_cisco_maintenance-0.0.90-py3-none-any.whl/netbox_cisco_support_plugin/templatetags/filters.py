from datetime import datetime, date
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


def is_expired(value):
    """
    Helper Function
    """
    return value < datetime.now().date()


def expires_next_year(value):
    """
    Helper Function
    """
    return value < date(date.today().year + 1, 12, 31)


@register.filter(is_safe=True)
def expiration_class(value):
    """
    Set CSS class for date fields
    """
    if not value or value == "None":
        return mark_safe('class="danger"')

    if is_expired(value):
        return mark_safe('class="danger"')
    elif expires_next_year(value):
        return mark_safe('class="warning"')


@register.filter(is_safe=True)
def coverage_class(value):
    """
    Set CSS class for text fields
    """
    if not value or value == "None":
        return mark_safe('class="danger"')


@register.filter(is_safe=True)
def boolian_class_success_true(value):
    """
    Set CSS class for boolian fields to display a green thick or a red cross
    """
    return (
        mark_safe('class="mdi mdi-check-bold text-success"')
        if value
        else mark_safe('class="mdi mdi-close-thick text-danger"')
    )


@register.filter(is_safe=True)
def boolian_class_failed_true(value):
    """
    Set CSS class for boolian fields to display a green thick or a red cross
    """
    return (
        mark_safe('class="mdi mdi-close-thick text-danger"')
        if value
        else mark_safe('class="mdi mdi-check-bold text-success"')
    )


@register.filter(is_safe=True)
def desired_match_recommended_release(desired_release, recommended_release):
    """Check if the desired release match the recommended release"""
    if not all (isinstance(value, str) for value in [desired_release, recommended_release]):
        return 'class="warning"'

    if desired_release not in recommended_release:
        return 'class="warning"'


@register.filter(is_safe=True)
def current_match_desired_release(current_release, desired_release):
    """Check if the desired release match the recommended release"""
    if not all (isinstance(value, str) for value in [current_release, desired_release]):
        return 'class="danger"'

    if current_release not in desired_release:
        return 'class="danger"'

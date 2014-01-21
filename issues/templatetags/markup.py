from django import template
from django.utils.safestring import mark_safe

import markdown as m

register = template.Library()


@register.filter(name='markdown')
def markdown(txt=None, extras=None):
    '''
        Placeholder to take care of some old template things in django 1.6
    '''
    if txt is None:
        return
    #
    if extras is None:
        extras = ["nl2br", ]  # to allow myself and others to be lazy...
    else:
        extras = ["nl2br", ]  ## i'm not sure what else right now...
    #
    return mark_safe(m.markdown(txt, extras, safe_mode=True, enable_attributes=False))

from django import template
from design import models as design_models
from member import models as member_models
from managing import models as managing_models
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag(takes_context=True)
def group_employees(context):
    if context['request'].user.pk:
        employees= managing_models.Employees.objects.filter(user_id=context['request'].user.pk)
        for i in employees:
            context['group_name'] = i.get_group_display()
        return context

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addhidden')
def addhidden(value):
    return value.as_widget(attrs={'style': 'display:none'})

@register.filter(name='adddisabled')
def adddisabled(value, arg):
    return value.as_widget(attrs={'disabled': arg})
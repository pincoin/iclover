from django import template
from design import models as design_models
from member import models as member_models

register = template.Library()


@register.simple_tag
def sample_list(slug, count=12):
    posts = member_models.Sample.objects.select_related('sectors_category__parent','employees__user').filter(
        sectors_category__in=design_models.SectorsCategory.objects.filter(slug=slug).get_descendants(include_self=True))[:count]
    return posts

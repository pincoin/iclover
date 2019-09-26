from django import template
from design import models as design_models
from member import models as member_models
from managing import models as managing_models

register = template.Library()

#
# @register.simple_tag
# def sample(slug, count=10):
#     posts = managing_models.Sample.objects.filter(state=True)[:count]
#         # sectors_category__in=design_models.SectorsCategory.objects.all().get_descendants(include_self=True))[:count]
#     return posts
#

from django import template
from main.models import Lesson, Click, ParticipationCount
from django.urls import reverse
from accounts.models import CustomUser



register = template.Library()






# All these 5 tags displays the number of participations for each belt color.

@register.simple_tag(takes_context=True)
def user_limit(context):
    # Gets you the limit for number of members.

    request = context['request']
    if request.user.is_authenticated:
        user_limit = CustomUser.objects.get(id=request.user.id).user_limit
        return user_limit
    return 0

@register.simple_tag
def get_customuser_count():
    # Gets you the number of members.

    return CustomUser.objects.count()

@register.filter(name='sort_by_day_order')
def sort_by_day_order(value):
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return sorted(value, key=lambda lesson: day_order.index(lesson.day))











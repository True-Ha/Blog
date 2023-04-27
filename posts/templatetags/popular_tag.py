# -*- coding: utf-8 -*-
 
from django import template
from django.db.models import Sum
from django.utils import timezone
 
from posts.models import Post
 
register = template.Library()
 
 
@register.simple_tag
def get_popular_articles_for_week():
 
    popular = Post.objects.filter(
        # filter records in the last 7 days
        date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]
    ).values(
        # Taking the field of interest to us, namely, the id and the title
        # Unfortunately we can not to pick up an object on the foreign key in this case 
        # Only the specific field of the object
        'slug'
    ).annotate(
        # Summing over rated recording
        sum_views=Sum('views')
    ).order_by(
        # sort the records Descending
        '-sum_views')[:5]    # Take 5 last records
 
    return popular
# post_id__title 'post_id__views',
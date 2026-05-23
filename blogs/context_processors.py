from .models import Category
from assignments.models import SocialLink

def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)


def get_social_links(request):
    social_links = SocialLink.objects.filter(link__isnull=False).exclude(link__exact='').order_by('platform')
    return dict(social_links=social_links)

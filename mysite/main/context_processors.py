from .models import Tag

# Menu function that returns tags queryset
def menu(request):
    nav_tags = Tag.objects.all()[:4]
    return {'nav_tags': nav_tags,}

from courses.models import Tags
from cart.cart import Cart

# Usage: to enable tags to all templates

def tags_processor(request):
    tags = Tags.objects.all()
    return {'tags': tags}

def cart(request):
    return {'cart': Cart(request)}


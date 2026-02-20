from .cart import Cart  

# Create a content_processor

def cart(request):
    # Return the default data
    return {'cart': Cart(request)}  






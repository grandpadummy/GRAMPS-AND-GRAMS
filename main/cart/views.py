from django.shortcuts import render, get_object_or_404
from urllib3 import request
from django.contrib import messages
from .cart import Cart
from app.models import Product
from django.http import JsonResponse

def cart_summary(request):
#     Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
#  Get the cart 
     cart = Cart(request)
# Test for post method 
     if request.POST.get('action') == 'post':  
          # Get Stuff
          product_id = int(request.POST.get('product_id'))
          # Add the quantity here
          product_qty = int(request.POST.get('product_qty'))
          # Look up product in db
          product = get_object_or_404(Product, id=product_id)
          # Save to a session
          cart.add(product=product, quantity=product_qty)
          # Return a response

          # Get cart quantity
          cart = cart_quantity = cart.__len__()

          # response = JsonResponse({'Product Name': product.name}) 
          # return response
          response = JsonResponse({'qty': cart_quantity}) 
          messages.success(request, ("Product has been added to cart."))
          return response

def cart_update(request):
     cart = Cart(request)
     if request.POST.get('action') == 'post':
          product_id = int(request.POST.get('product_id'))
          product_qty = int(request.POST.get('product_qty'))

          cart.update(product=product_id, quantity=product_qty)

          response = JsonResponse({'success': 'Product quantity updated'})
          return response

def cart_delete(request):
     cart = Cart(request)
     if request.POST.get('action') == 'post':
          product_id = int(request.POST.get('product_id'))
          cart.delete(product=product_id)

          response = JsonResponse({'success': 'Product removed from cart'})
          return response










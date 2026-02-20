from ast import Delete
from django.shortcuts import redirect, render
from django.contrib import messages
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from cart.cart import Cart
from django.contrib.auth.models import User
from app.models import Product, Profile
import datetime




def checkout(request):
    #   Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Shipping User
        shipping_user = ShippingAddress.objects.filter(shipping_user=request.user).first()
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals, 'shipping_form': shipping_form})
    else:
        # Check out as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals, 'shipping_form': shipping_form})

    


def payment_success(request):
    messages.success(request, 'Payment processed successfully.')
    return render(request, 'payment/payment_success.html')

def billing_info(request):
    if request.POST:

        #   Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()
        # Create a session
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        

            # Check to see if logged in
        if request.user.is_authenticated:
            # Get Billing Form
            billing_form = PaymentForm()
            
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals, 'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            # Not logged in
            # Get Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals, 'shipping_info': request.POST, 'billing_form': billing_form})
    
        shipping_form = request.POST

        return render(request, 'payment/billing_info.html', {'cart_products': cart_products, "quantities": quantities, "totals": totals, 'shipping_form': shipping_form})
    else:
        messages.success(request, 'Invalid access to billing information page.')
        return redirect('home')
   

    

def process_order(request):
    if request.POST:

        #   Get the cart
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        totals = cart.cart_total()

        # Get billing info

        payment_form = PaymentForm(request.POST or None)
        # Get Shipping Stuff
        my_shipping = request.session.get('my_shipping')
        # print(my_shipping)
       
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']  
        email = my_shipping['shipping_email'] 
        
        # Create shipping address from session

        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zip_code']}\n{my_shipping['shipping_country']}"
        # print(shipping_address)

        amount_paid = totals

        # Create order here

        if request.user.is_authenticated:
            # Logged in
            user = request.user
            # Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address1=shipping_address, amount_paid=amount_paid)
            create_order.save()
            # Create Order Items
            
            order_id = create_order.pk
            # Get product id
            for product in cart_products:
                product_id = product.id

                if product.on_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key,value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user,  quantity=value, price=price)
                        create_order_item.save()


            # Delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]

            # Delete cart from database (old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            # Delete shopping cart in database
            current_user.update(old_cart="") 

            messages.success(request, 'Order Placed Successfully.')
            return redirect('home') 

        else:
            # not logged in
            create_order = Order(full_name=full_name, email=email, shipping_address1=shipping_address, amount_paid=amount_paid)
            create_order.save()

              # Create Order Items
            
            order_id = create_order.pk
            # Get product id
            for product in cart_products:
                product_id = product.id

                if product.on_sale:
                    price = product.sale_price
                else:
                    price = product.price

                for key,value in quantities.items():
                    if int(key) == product_id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()

            # Delete the cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]


            messages.success(request, 'Order Placed Successfully.')
            return redirect('home') 


         
    else:
        messages.error(request, 'Invalid access to process order.')
        return redirect('home')   
    


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)
            order.update(shipped=True, date_shipped=now)
                
            messages.success(request, 'Order marked as shipped.')
            return redirect('home')

        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'Access Denied.')
        return redirect('home') 


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num = request.POST['num']
            now = datetime.datetime.now()
            order = Order.objects.filter(id=num)
            order.update(shipped=False)
                
            messages.success(request, 'Order marked as not shipped.')
            return redirect('home')

        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})


    
    else:
        messages.success(request, 'Access Denied.')
        return redirect('home') 
    
def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        # Get the Order
        order = Order.objects.get(id=pk)
        # Get the order items
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            if status == 'true':
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
                messages.success(request, 'Order marked as shipped.')
                return redirect('shipped_dash')
            else:
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=False)
                messages.success(request, 'Order marked as not shipped.')
                return redirect('not_shipped_dash')

        return render(request, 'payment/orders.html', {'order': order, 'items': items})
    else:
        messages.success(request, 'Access Denied.')
        return redirect('home') 



# order.shipped = True
            
#                 now = datetime.datetime.now()
#                 order.save()


# order.shipped = False
                
#                 now = datetime.datetime.now()
#                 order.save()






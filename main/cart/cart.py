from app.models import Product, Profile



class Cart():
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request

        # Need to get the current session key
        cart = self.session.get('session_key')

        # If the user is new, no session key Create one
        if 'session_key' not in self.session:
            cart = self.session['session_key'] = {}

        # Make sure the cart is on every page

        self.cart = cart


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # Logic

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to Profile model
            current_user.update(old_cart=str(carty))    
         

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to Profile model
            current_user.update(old_cart=str(carty))                                          
    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        

        quantities= self.cart
        total = 0
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == (key):
                    if product.on_sale:
                       total += (product.sale_price * value) 
                    else:
                        total += (product.price * value)
        return total
                
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to look up prroduct in database
        products = Product.objects.filter(id__in=product_ids)
        # Return products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities


    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] = product_qty
        self.session.modified = True
 
        

          # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to Profile model
            current_user.update(old_cart=str(carty)) 
         
        thing = self.cart
        return thing


    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

          # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert to double quotes
            carty = str(self.cart)
            carty = carty.replace("\'", '\"')
            # Save carty to Profile model
            current_user.update(old_cart=str(carty))                  































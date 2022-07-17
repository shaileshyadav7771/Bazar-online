from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem


# Create your views here.

# we will create Private function which will take session ID from request And store it for Card ID.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)  # get the product
    print("Product : ", product)
    try:
        # we need session ID to store
        cart = Cart.objects.get(Cart_id=_cart_id(request))
        print("cart :", cart)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            Cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1  # current_item quantity + 1
        cart_item.save()
    # means we'll create new card Item and quantity will be 1
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart, )
    cart_item.save()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(Cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (18 * total)/100
        grand_total = total + tax
    except:
        pass

    # passing all value to html template
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "tax"       : tax,
        "grand_total" : grand_total,
    }

    return render(request, 'store/cart.html', context)

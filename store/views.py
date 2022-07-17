from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem

# Create your views here.

def store(request, category_slug=None):
    categorys = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        product_counts = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_counts = products.count()

    context = {
        'products': products,
        'product_counts': product_counts,
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        print(" single_product :", single_product)
        #logic for what if card already added in detail page (we should not show add card again.)
        in_cart = CartItem.objects.filter(cart__Cart_id=_cart_id(request),product=single_product).exists()
        print("in_cart : ", in_cart)

    except Exception as e:
        raise e
    context = {'single_product': single_product,
               'in_cart' : in_cart,
               }

    return render(request, 'store/product_detail.html', context)

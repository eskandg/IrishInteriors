from .models import *
from .forms import *
from .serializers import *
from .permissions import admin_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
import json
from rest_framework import viewsets, permissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class UserViewSet(viewsets.ModelViewSet):
    queryset = CaUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def check_registration(self, registration_data):
        try:
            CaUser.objects.get(username=registration_data["username"])
            return "User already exists."
        except CaUser.DoesNotExist:
            pass

        if registration_data["password1"] == registration_data["password2"]:
            return True

        return "Passwords don't match."

    def post(self, request):  #
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        check = self.check_registration(body)

        user = CASignUpForm(body)
        if user.is_valid() and check:
            new_user = user.save()
            login(self.request, new_user)
        elif check != True:
            return JsonResponse({"error": check})
        else:
            check = "Password criteria not met."
            return JsonResponse({"error": check})

        return JsonResponse(body)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = []


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer


@method_decorator(csrf_exempt, name='dispatch')
class CaUserSignUpView(CreateView):
    model = CaUser
    form_class = CASignUpForm
    template_name = "registration.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class AdminSignUpView(CreateView):
    model = CaUser
    form_class = AdminSignUpForm
    template_name = "admin_registration.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


def index(request):
    format = request.GET.get("format", "")
    categories = ProductCategory.objects.all()

    if format == "json":
        categories_serialised = serializers.serialize("json", categories)
        return HttpResponse(categories_serialised, content_type="application/json")

    return render(request, 'index.html', {'categories': categories})


def products(request, category_name=None):
    format = request.GET.get("format", "")

    site = request.path
    sitename = site[10:]  # category name

    categories = ProductCategory.objects.all()
    if category_name == None:
        all_p = Product.objects.all()

        if format == "json":
            products_serialised = serializers.serialize("json", all_p)
            return HttpResponse(products_serialised, content_type="application/json")

        return render(request, 'products.html', {'products': all_p, 'categories': categories})

    try:
        product_category = ProductCategory.objects.get(name=category_name)
        category_products = Product.objects.filter(category=product_category)
        if format == "json":
            products_serialised = serializers.serialize("json", category_products)
            return HttpResponse(products_serialised, content_type="application/json")

        return render(request, 'products.html',
                      {'products': category_products, 'categories': categories, 'failed_category': False,
                       'sitename': sitename})

    except ProductCategory.DoesNotExist:
        all_p = Product.objects.all()
        return render(request, 'products.html', {'products': all_p, 'categories': categories,
                                                 'failed_category': True})  # sends us to products with an alert


def product(request, product_id, added=False):
    try:
        prod = Product.objects.get(pk=product_id)

        # get products related by category
        category_products = list(Product.objects.filter(category=prod.category))
        category_products.remove(prod)  # get rid of the product that has the same id as the one in the url
        size = len(category_products)

        first_category_product = None
        try:
            first_category_product = category_products[0]  # for the carousel active item
        except IndexError:
            pass

        category_products = category_products[1:]  # get the rest of the carousel items

        return render(request, "product.html", {"product": prod,
                                                "added": added,
                                                'first_category_product': first_category_product,
                                                'category_products': category_products,
                                                'category_products_size': size}
                      )

    except Product.DoesNotExist:
        all_products = Product.objects.all()
        categories = ProductCategory.objects.all()
        return render(request, 'products.html',
                      {'products': all_products, 'categories': categories, 'failed_category': False,
                       'failed_product': True})


@login_required
@admin_required
def product_form(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save()
            return render(request, "product.html", {'product': new_product})
    else:
        form = ProductForm()
        return render(request, 'form.html', {'form': form})


class Login(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return redirect('/')


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def basket(request):
    user = request.user
    if user.is_anonymous:
        try:
            token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        except AttributeError:
            return redirect("login")
        user = Token.objects.get(key=token).user
    site = request.path

    shopping_basket = None
    try:
        shopping_basket = ShoppingBasket.objects.get(user_id=user)
    except ShoppingBasket.DoesNotExist:
        shopping_basket = ShoppingBasket(user_id=user)
        shopping_basket.save()

    try:
        basket_items = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
        basket_items_list = list(basket_items)

        products = [(Product.objects.get(pk=item.product_id_id), item.quantity) for item in basket_items_list]
        total_price = 0
        size = 0
        for p in products:
            size += p[1]
            total_price += p[0].price * p[1]

        flag = request.GET.get('format', '')
        if flag == "json":
            basket_array = []
            for basket_item in products:
                product_dict = {
                    'name': basket_item[0].name,
                    'price': str(basket_item[0].price),
                    'category': basket_item[0].category.name.capitalize(),
                    'quantity': int(basket_item[1]),
                }

                basket_array.append(product_dict)

            return HttpResponse(json.dumps({"items": basket_array, "size": size, "total_price": str(total_price)}),
                                content_type="application/json")
        else:
            return render(request, 'basket.html',
                          {"products": products, "items": basket_items_list, "size": size, 'total_price': total_price})
    except ShoppingBasket.DoesNotExist:
        return render(request, 'basket.html', {"size": 0})


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_to_basket(request, product_id):
    user = request.user
    flag = request.GET.get("format", "")

    if user.is_anonymous:
        if flag == "json":
            token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
            user = Token.objects.get(key=token).user
        else:
            return redirect("login")

    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

    if shopping_basket is None:
        ShoppingBasket(user_id=user).save()
        shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

    prod = Product.objects.get(pk=product_id)
    basket_item = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id, product_id=prod.id).first()

    if basket_item is None:
        basket_item = ShoppingBasketItems(basket_id=shopping_basket, product_id=prod).save()
    else:
        basket_item.quantity += 1
        basket_item.save()

    if flag == "json":
        return JsonResponse({'status': 'success'})
    else:
        return product(request, product_id, added=True)


@login_required
def add_from_basket(request, product_id):
    user = request.user

    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

    if shopping_basket is None:
        shopping_basket = ShoppingBasket(user_id=user).save()

    prod = Product.objects.get(pk=product_id)
    basket_item = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id, product_id=prod.id).first()
    if basket_item is None:
        basket_item = ShoppingBasketItems(basket_id=shopping_basket, product_id=prod).save()

    else:
        basket_item.quantity += 1
        basket_item.save()

    return redirect('/basket')


@login_required
def remove_from_basket(request, product_id):
    user = request.user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

    if shopping_basket is None:
        shopping_basket = ShoppingBasket(user_id=user).save()

    prod = Product.objects.get(pk=product_id)
    basket_item = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id, product_id=prod.id).first()
    if basket_item is not None:
        if basket_item.quantity != 0:
            basket_item.quantity -= 1

        if basket_item.quantity == 0:
            basket_item.delete()
        else:
            basket_item.save()

    return redirect('/basket')


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
@csrf_exempt
def order_form(request):
    user = request.user
    if user.is_anonymous:
        token = request.META.get('HTTP_AUTHORIZATION').split(" ")[1]
        user = Token.objects.get(key=token).user
    shopping_basket = ShoppingBasket.objects.filter(user_id=user).first()

    if not shopping_basket:
        return redirect(request, '/basket')

    basket_items = ShoppingBasketItems.objects.filter(basket_id=shopping_basket.id)
    basket_items_list = list(basket_items)

    subtotal = 0
    for item in basket_items:
        subtotal += (item.product_id.price * item.quantity)

    total_price = subtotal + 8  # Shipping Fee
    if request.method == 'POST':
        if not request.POST:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            order = OrderForm(body)
        else:
            order = OrderForm(request.POST)

        flag = request.GET.get("format", "")
        if order.is_valid() and len(basket_items) != 0:  # order complete
            new_order = order.save(commit=False)
            new_order.user_id = user
            new_order.save()

            shopping_basket.delete()
            empty_shopping_basket = ShoppingBasket(user_id=user).save()

            order_items = []
            for item in basket_items:
                order_item = OrderItems(order_id=new_order, product_id=item.product_id_id, quantity=item.quantity)
                order_items.append(order_item)

            if flag == "json":
                order_credentials = {"id": new_order.id,
                                     "cardholder_name": new_order.cardholder_name,
                                     "shipping_address": new_order.shipping_address,
                                     "date_created": new_order.date_created,
                                    }

                order_items_array = []
                for order_item in order_items:
                    order_items_dict = {
                        'name': order_item.product.name,
                        'price': str(order_item.product.price),
                        'quantity': int(order_item.quantity),
                    }

                    order_items_array.append(order_items_dict)

                return JsonResponse({'order_credentials': order_credentials,
                                     'order_items': order_items_array,
                                     'subtotal': subtotal,
                                     'total_price': total_price})

            else:
                return render(request, "order_complete.html",
                              {'order': new_order, 'order_items': order_items, 'subtotal': subtotal,
                               'total_price': total_price})
        else:
            if flag == "json":
                return JsonResponse({'Error': "Order has already been placed."})
    else:  # checkout

        order = OrderForm()
        return render(request, 'checkout.html',
                      {'order': order, 'basket': shopping_basket, 'basket_items': basket_items_list,
                       'subtotal': subtotal, 'total_price': total_price})

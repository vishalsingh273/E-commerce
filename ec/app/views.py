from django.shortcuts import render, redirect, HttpResponse
from django.views import View
from .models import Product, Customer,Cart
from django.db.models import Count
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout

# Create your views here.

def logout_view(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
        # Redirect to a page after logout
        return redirect('login') 

def home(request):
    return render(request, 'app/home.html')


def about(request):
    return render(request, 'app/about.html')


def contact(request):
    return render(request, 'app/contact.html')

def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    return render(request,"app/addtocart.html", locals())

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')

        return render(request, 'app/category.html', locals())


class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(
            category=product[0].category).values('title')
        return render(request, "app/category.html", locals())


class ProductDetails(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'app/product-detail.html', locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Congratulations ! your registered successfully..')

        else:
            messages.error(request, "Invalid data entered ")

        return render(request, 'app/customerregistration.html', locals())


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality,
                           city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(
                request, "Your profile has been created successfully!!")
        else:
            messages.error(request, "Error while creating the profile")

        return render(request, 'app/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', locals())


class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateaddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']

            add.save()
            messages.success(
                request, "Your profile has been updated successfully!!")
        else:
            messages.error(request, "Error while updating the profile")
        return redirect('address')



from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import Contact, Product, Order, OrderUpdate
from math import ceil
import json


# Create your views here.

def index(request):
    allProds = []
    first3 = Product.objects.all()[0:3]
    first4 = Product.objects.all()[0:4]
    first8 = Product.objects.all()[0:8]
    context = {
        "first3":first3,
        "first8":first8,
        "first4":first4,
    }
    return render(request, 'shop/index.html', context)

def shop(request):
    categoryProds = Product.objects.values('category')
    category = {item['category'] for item in categoryProds}
    allProds = Product.objects.all()
    context = {
        "category": category,
        "allProds":allProds
    }
    return render(request, 'shop/shop.html', context)

def searchMatch(query, item):
    print(query, item)
    ''' Return true only if query matches the item '''
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        print('true')
        return True
    else:
        print('false')
        return False

def search(request):
    query = request.GET.get('query')
    query = query.lower()
    allProds = []
    categoryProds = Product.objects.values('category')
    category = {item['category'] for item in categoryProds}
    allProds = Product.objects.all()
    prods = [item for item in allProds if searchMatch(query, item)]
    if len(prods) != 0:
        context = {
            "category":category,
            "prods":prods,
        }
    return render(request, 'shop/search.html', context)
    if len(allProds) == 0 or len(query) <3 :
        params = {'msg': 'please enter valid value'}
    return render(request, 'shop/search.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contacts = Contact(name=name, email=email, subject=subject, message=message)
        contacts.save()
        messages.success(request, 'Your Message has been submitted succesfully')
        redirect('/contact')
    return render(request, 'shop/contact.html')

def about(request):
    return render(request, 'home/about.html')

def handleSignup(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        special_chars = """~,.?{()}`/#@!&*%_-='"<>:;"""
        if len(fname)<3 or len(lname)<3 or len(email)<13 or len(pass1)<8:
            messages.error(request, 'Please enter valid details')


        if pass1 == pass2:
            count = 0
            upper = 0
            for characters in pass1:
                if characters in special_chars:
                    count = count + 1
            if characters.isupper():
                upper = upper + 1
            if upper == 0:
                messages.warning(request, 'At least one character in passsword must be in Uppercase')
            if count == 0:
                messages.warning(request, 'Your password most be with special characters')
            # ----------------Check if the user already exist----------------------------#
            try:
                # ----------------Try creating the user----------------------------#
                myuser = User.objects.create_user(email, email, pass1)
                myuser.first_name = fname
                myuser.last_name = lname
                myuser.save()
                messages.success(request, 'Your Shopping Account has been created successfully')
                return redirect( '/')
                
            except Exception as e:
                messages.warning(request, 'Your account already exists with this email address')
            
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('/')

    return render(request, 'shop/register.html')

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('loginemail')
        password = request.POST.get('loginpass')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Loged in successfully')
            return redirect( '/')
        else:
            messages.error(request, 'Invalid credencials.Please try again')
            return redirect( '/')
    return render(request, 'shop/login.html')

def handleLogout(request):
    logout(request)
    return redirect('/')

def prodView(request, product_id):
    post = Product.objects.filter(product_id=product_id).first()
    context = {
        'post':post,
        "category":post.category
    }
    return render(request, 'shop/single-product.html', context)

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        address2 = request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(items_json=items_json, name=name, email=email, phone=phone, address=address, address2=address2, city=city, state=state, zip_code=zip_code, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'home/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'home/checkout.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status': 'success', 'updates': updates, 'itemsJason': order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "noitem"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')

    return render(request, 'home/tracker.html')

from home.models import Contact, Product, Order, OrderUpdate, PostComment
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth.models import User
from home.templatetags import extras
from django.contrib import messages
from math import ceil
import json


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
                if characters.isupper()==True:
                    upper = upper + 1
            if upper == 0:
                messages.warning(request, 'At least one character in passsword must be in Uppercase')
                return redirect('/signup')
            if count == 0:
                messages.warning(request, 'Your password most be with special characters')
                return redirect('/signup')
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
            return redirect('/signup')

    return render(request, 'shop/signup.html')


def handleLogin(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Loged in successfully')
            return redirect( '/')
        else:
            messages.error(request, 'Invalid credencials.Please try again')
            return redirect( '/login')
    return render(request, 'shop/login.html')


def handleLogout(request):
    logout(request)
    return redirect('/')


def searchMatch(query, item):
    ''' Return true only if query matches the item '''
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower() or query in item.subcategory.lower():
        return True
    else:
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
    return render(request, 'shop/about.html')


def prodView(request, product_id):
    post = Product.objects.filter(product_id=product_id).first()
    comments = PostComment.objects.filter(post=post, parent=None)
    replies = PostComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    context = {
        'post':post,
        "category":post.category,
        "id":product_id,
        "comments": comments,
        'repDict':repDict,
    }
    return render(request, 'shop/product.html', context)


def cart(request):
    return render(request, 'shop/cart.html')


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('add1', '')
        address2 = request.POST.get('add2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        order = Order(items_json=items_json, name=name, email=email, phone=phone, address=address, address2=address2, city=city, state=state, zip_code=zip_code, amount=amount, payment="esewa")
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email).first()
            if order:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append([item.update_desc, str(item.timestamp)])
                all = json.loads(order.items_json).values()
                total = 0
                for qty, name, price, sno in all:
                    amount = int(price[3:])
                    no = int(qty)
                    total = total + (qty*amount)
                context = {
                    "items":all,
                    "updates":updates,
                    "order_no": orderId,
                    "city":order.city,
                    "zip_code":order.zip_code,
                    "state":order.state,
                    "address": order.state,
                    "date": order.timestamp,
                    "payment":order.payment,
                    "total":total,


                }
                return render(request, 'shop/details.html', context)
            else:
                return HttpResponse('{"status": "noitem"}')
        except Exception as e:
            return HttpResponse('{"status": "error"}')


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user =  request.user
        post_id =  request.POST.get("post_id")
        product = Product.objects.get(product_id=post_id)
        parentsno = request.POST.get('parentsno')
        if parentsno =="":
            comment = PostComment(comment=comment, user=user, post=product)
            messages.success(request, 'Successfully Commented')
        else:
            parent  = PostComment.objects.get(sno=parentsno)
            comment = PostComment(comment=comment, user=user, post=product, parent=parent)
            messages.success(request, 'Successfully Replied')
        comment.save()
        return  redirect(f"/{post_id}")
    else:
        return HttpResponse('404-page not found')
    return redirect(f"/{post_id}")


def handlePayment(request):
    # Handle your payment here
    pass


def nopage(request, nopage):
    return HttpResponse('Page Not Found')
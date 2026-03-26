import random
from django.shortcuts import get_object_or_404, render,redirect
from .models import Product,Category,CustomUser
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .utils import encrypt_password, decrypt_password
import time
from datetime import timedelta
import requests
from django.utils import timezone

MAX_ATTEMPTS = 7
LOCK_MINUTES = 1

def home (request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price =request.POST.get('price')
        qunt = request.POST.get('qunt')
        desc = request.POST.get('desc')
        category = Category.objects.get(id=request.POST['category'])        
        img = request.FILES['img']

        obj = Product.objects.create(
            name = name,
            price = price,
            qunt = qunt,
            category = category,
            desc = desc,
            img = img,
        )
        obj.save()

    categories = Category.objects.all()
    return render(request,'home.html',{"cat":categories})

def pd (request):
    pd = Product.objects.all()
    return render(request,'pd.html',{'prd':pd})

def delete (request,id):
    pd = Product.objects.get(id=id)
    pd.delete()
    return redirect('pd')

def edit(request,id):
    pli = Product.objects.get(id=id)
    if request.method == 'POST' :
        pli.name = request.POST.get('name')
        pli.price = request.POST.get('price')
        pli.qunt = request.POST.get('qunt')

        if request.FILES.get('img'): 
            pli.img = request.FILES['img']
        pli.save()

        return redirect('pd')
    else:
        return render(request,'edit.html',{"prd":pli})

def about(request,id):
    sp = Product.objects.get(id=id)
    return render(request,'show_pro.html',{'item':sp})

# def cart(request,id):
#     cart = Product.objects.get(id=id)
#     return render(request,'cart.html',{'ac':cart})

def addcat(request):
    if request.method == 'POST':
        cat = request.POST.get('cat')
        img = request.FILES['img']
        cobj = Category.objects.create(
            cat = cat,
            img = img,
        )
        cobj.save()
        return redirect('cl')
    return render(request,'addcat.html')

def cl(request):
    cli = Category.objects.all()
    return render(request,'cl.html',{'cd':cli})

def editcat(request,id):
    cli = Category.objects.get(id=id)
    if request.method == 'POST' :
        cli.cat = request.POST.get('cat')      
        
        if request.FILES.get('img'): 
            cli.img = request.FILES['img']
        cli.save()  
        cli.save()

        return redirect('cl')
    else:
        return render (request,'editcat.html',{"ce":cli})

def deletecat (request,id):
    cl = Category.objects.get(id=id)
    cl.delete()
    return redirect('cl')

def cate_pro(request,id):
    pro = Product.objects.filter(category=id)
    return render(request,'cate_pro.html',{'catp':pro})


def cart_view (request):
    cart = request.session.get("cart",{})
    msg = "User Not Found"

    total_amount = 0

    for item in cart.values():
        total_amount += (item["price"]) * item["qunt"]

    return render(request,'cart_view.html',{"cart_view":cart,"total_amount":total_amount,"msg":msg})

def add_cart (request,id):
    atoc = get_object_or_404(Product,id=id)
    cart = request.session.get("cart",{})
    
    if str(id) in cart: 
        cart[str(id)]["qunt"] += 1

    else:
        cart[str(id)]={
            "name" : atoc.name,
            "price" : atoc.price,
            "qunt" : atoc.qunt,
            "desc" :atoc.desc,
            "img" : atoc.img.url if atoc.img else None,
        }
        
        request.session["cart"] = cart
        request.session.modified = True
    return redirect("cart_view")

def buy (request):
    return render(request,'buy.html')

def remove_cart(request,id):
    cart = request.session.get("cart",{})

    print(cart)
    print(id)
    if str(id) in cart:
        del cart[str(id)]
        request.session["cart"] = cart
        
    
        # for item in cart.values():
        #     total_amount -= (item["price"]) * item["qunt"]


    return redirect("cart_view")

def show_pro(request,id):
    sp = Product.objects.get(id=id)
    return render(request,'show_pro.html',{'item':sp})

def update_cart(request,id,action):
    cart = request.session.get("cart",{})

    if str(id) in cart:
        if action == "increase":
            cart[str(id)]["qunt"] += 1

        elif action == "decrease":
            if cart[str(id)]["qunt"] > 1:
                cart[str(id)]["qunt"] -= 1
            else:
                del cart[str(id)]

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart_view")


def register(request):

    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        key = int(request.POST['key'])
        phone = request.POST['phone']

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            context['error'] = "Username already taken!"
        else:
            # Encrypt password
            enc_pass = encrypt_password(password, key)
            # Create user
            user = CustomUser(username=username, password=enc_pass, key=key, phone=phone)
            user.save()
            return redirect('/login/')
    return render(request, 'register.html', context)


def login_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username)

            # Check if account is locked
            if user.attempts >= MAX_ATTEMPTS:
                if user.last_attempt and timezone.now() < user.last_attempt + timedelta(minutes=LOCK_MINUTES):
                    remaining = (user.last_attempt + timedelta(minutes=LOCK_MINUTES) - timezone.now()).seconds
                    context['error'] = f"Account locked. Try after {remaining} seconds."
                    context['timer'] = remaining
                    return render(request, 'login.html', context)
                else:
                    user.attempts = 0  # reset attempts after lock time
                    user.save()

            entered_encrypted = encrypt_password(password, user.key)

            if entered_encrypted == user.password:
                user.attempts = 0
                user.save()
                return render(request, 'home.html')
            else:
                user.attempts += 1
                user.last_attempt = timezone.now()
                user.save()

                context['error'] = "Wrong Password!"
                context['clue'] = f"Encrypted Pass: {user.password} | Key: {user.key}"
                context['remaining'] = MAX_ATTEMPTS - user.attempts

        except CustomUser.DoesNotExist:
            context['error'] = "User Not Found!"
            context['clue'] = None

    return render(request, 'login.html', context)


def forgot_password(request):

    if request.method == "POST":

        phone = request.POST['phone']

        otp = random.randint(1000,9999)

        otp_storage[phone] = otp

        print("OTP:",otp)  # console ma OTP

        return redirect('verify_otp')

    return render(request,'phone.html')


# temp store OTP in memory (for testing)

otp_storage = {}  # { phone: {'otp':1234, 'expiry':datetime} }

FAST2SMS_API_KEY = "gfqopWcTydRbxAUDG4meFz0h9NrXIQ52JaYZ3LMk16juvlsSi8HfJ1CwSNjhOLqMdrvx2gUPVoQKznBm"

# Send OTP via Fast2SMS
def send_otp_fast2sms(phone, otp):

    url = "https://www.fast2sms.com/dev/bulkV2"

    payload = {
        "route": "otp",
        "variables_values": otp,
        "numbers": phone
    }

    headers = {
        'authorization': FAST2SMS_API_KEY
    }

    response = requests.get(url, params=payload, headers=headers)

    print("Fast2SMS response:", response.json())


def forgot_phone_view(request):
    context = {}
    if request.method == "POST":
        phone = request.POST['phone']
        try:
            user = CustomUser.objects.get(phone=phone)
            otp = random.randint(1000,9999)
            expiry = timezone.now() + timedelta(minutes=5)
            otp_storage[phone] = {'otp': otp, 'expiry': expiry}

            send_otp_fast2sms(phone, otp)  # Send real OTP

            return redirect(f'/otp/?phone={phone}')
        except CustomUser.DoesNotExist:
            context['error'] = "Invalid phone number!"
    return render(request, 'phone.html', context)

def verify_otp(request):

    if request.method == "POST":

        phone = request.POST['phone']
        otp = request.POST['otp']

        if str(otp_storage[phone]['otp']) == otp:
            request.session['phone'] = phone

            return redirect('reset_password')

    return render(request,'otp.html')

def otp_view(request):
    context = {}
    phone = request.POST.get('phone') or request.GET.get('phone')
    if request.method == "POST":
        entered = request.POST['otp']
        otp_info = otp_storage.get(phone)
        if otp_info:
            if timezone.now() > otp_info['expiry']:
                context['error'] = "OTP expired! Request new OTP."
            elif str(otp_info['otp']) == entered:
                otp_storage.pop(phone)
                return redirect(f'/reset/?phone={phone}')
            else:
                context['error'] = "Wrong OTP!"
        else:
            context['error'] = "No OTP found! Request new OTP."
    return render(request, 'otp.html', context)

def reset_password(request):
    context = {}
    phone = request.GET.get('phone')
    if request.method == "POST":
        password = request.POST['password']
        confirm = request.POST['confirm']
        key = int(request.POST['key'])
        if password != confirm:
            context['error'] = "Passwords do not match!"
        else:
            try:
                user = CustomUser.objects.get(phone=phone)
                user.password = encrypt_password(password,key)
                user.key = key
                user.attempts = 0
                user.save()
                return redirect('/login/')
            except CustomUser.DoesNotExist:
                context['error'] = "User not found!"
    return render(request, 'reset.html', context)

def logout_view(request):
    # User logout
    logout(request)
    # Redirect to login page
    return redirect('login')


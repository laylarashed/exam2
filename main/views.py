from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import *
import bcrypt
import datetime

def root(request):
    return render(request, "index.html")

def register(request):
    request.session['action'] = "reg"

    errors = Users.objects.register_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        user = Users.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
        
        first_name = user.first_name
        user_id = user.id
        request.session['username'] = first_name
        request.session['id'] = user_id
        return redirect("/dashboard")

def login(request):
    request.session['action'] = "login"
    errors = Users.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = Users.objects.get(email=request.POST['email'])
        first_name = user.first_name
        user_id = user.id
        request.session['username'] = first_name
        request.session['id'] = user_id
        return redirect("/dashboard")



def dashboard(request):        
        context = {
            "other_wishes" : Wishes.objects.exclude(on_whish = request.session['id']),
            "user" : Users.objects.get(id=request.session['id']),
        }
        return render(request, "dashboard.html", context)


def new_wish(request):
    return render(request, "new_wish.html")

def create_wish(request):

    errors = Wishes.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/wishes/new")
    else:
        name = request.POST['name']
        description = request.POST['description']

        user = Users.objects.get(id=request.session['id'])
        wish = Wishes.objects.create(name=name, description=description, created_by=user)
        creater = Users.objects.get(id=request.session['id'])
        wish.on_whish.add(creater)
        return redirect("/dashboard")

def delete_wish(request, id):
    wish = Wishes.objects.get(id=id)
    wish.delete()
    return redirect("/dashboard")


def edit_wish(request, id):
    context = {
        "wish" : Wishes.objects.get(id=id),
    }
    return render(request, "edit.html", context)

def update_wish(request, id):
    errors = Wishes.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/edit/"+str(id))
    else:
        name = request.POST['name']
        description = request.POST['description']
        wish = Wishes.objects.get(id=id)
        wish.name = name
        wish.description = description
        wish.save()
        return redirect("/dashboard")


def wish_info(request):
    context = {
        "like" : Wishes.objects.all(),
        "count": Granted.objects.get(id=1),
        "user": Users.objects.get(id=request.session['id']),
        "granted" : len(Users.objects.get(id=request.session['id']).wishes.all()),
    }
    return render(request, "wish_info.html", context)


def like_wish(request, id):
    wish = Wishes.objects.get(id=id)
    # user = Users.objects.get(id=request.session['id'])
    # wish.on_whish.add(user)
    wish.like +=1
    wish.save()

    return redirect("/dashboard")

def cancel_wish(request, id):
    wish = Wishes.objects.get(id=id)
    user = Users.objects.get(id=request.session['id'])
    user.date_granted=datetime.datetime.now()
    Granted.objects.create(count = 0)
    granted = Granted.objects.get(id=1)
    granted.count +=1
    user.granted +=1
    user.save()
    granted.save()
    user.wishes.remove(wish)

    return redirect("/dashboard")


def logout(request):
    request.session.flush()
    return redirect("/")
from django.db import models
import re, datetime
import bcrypt
# Create your models here.

class UsersManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['first_name'] = "First name should be at least 2 characters"
        if len(postData['lname']) < 2:
            errors['last_name'] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Please enter a valid email address!"
        elif len(Users.objects.filter(email=postData['email'])) > 0:
            errors['used'] = "Email address is already in use"
        if len(postData['password']) < 8:           
            errors['password'] = "Password should be at least 8 characters"

        if postData['password'] != postData['conf_pass']:
            errors['mismatch'] = "Passwords should match"

        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if not EMAIL_REGEX.match(postData['email']):            
            errors['login_email'] = "Please enter a valid email address!"

        if len(Users.objects.filter(email = postData['email'])) == 0:
            errors['email'] = "Email or password is incorrect"
        else:
            user = Users.objects.filter(email = postData['email'])
            user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors['email'] = "Email or password is incorrect"

        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    granted =models.IntegerField(default = 0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()


class WishesManager(models.Manager):
    def wish_validator(self, postData):
        errors = {}
        
        if len(postData['name']) < 3:
            errors['name'] = "A Wish Name must be at least 3 characters"
        if len(postData['description']) < 1:
            errors['description'] = "A Wish Description must be provided"
        elif len(postData['description']) < 3:
            errors['description_length'] = "A Wish Description must be at least 3 characters"
        
        return errors


class Wishes(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    date_granted =models.DateField(auto_now=True)
    like = models.IntegerField(default = 0)
    created_by = models.ForeignKey(Users, related_name="wish", on_delete = models.CASCADE)
    on_whish = models.ManyToManyField(Users, related_name="wishes")



    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WishesManager()

class Granted(models.Model):
    count = models.IntegerField(default = 0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
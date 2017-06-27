from django.db import models
import bcrypt, re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, input):
        errors = []

        if len(input['first_name']) < 3:
            errors.append('First name must be at least 3 characters')

        if len(input['last_name']) < 3:
            errors.append('Last name must be at least 3 characters')

        if not input['first_name'].isalpha():
            errors.append('First name can contain letters only')

        if not input['last_name'].isalpha():
            errors.append('Last name can contain letters only')

        if not email_regex.match(input['email']):
            errors.append('Not a valid email')

        if len(input['email']) == 0:
            errors.append('Please enter an email')

        if input['password'] != input['confirm']:
            errors.append('Passwords do not match.')

        if len(input['password']) < 8:
            errors.append('Password must be at least 8 characters')

        same = User.objects.filter(email=input['email'])
        if same:
            errors.append('Email is already in use')

        if len(errors) == 0:
            pwHash = bcrypt.hashpw(input['password'].encode(), bcrypt.gensalt().encode())
            user = User.objects.create(first_name=input['first_name'], last_name=input['last_name'], email=input['email'], password=pwHash)
            return (True, user)

        else:
            return (False, errors)

    def login(self, input):
        errors = []
        user = User.objects.filter(email=input['email'])
        if user.exists():
            if bcrypt.checkpw((input['password'].encode()), (user[0].password.encode())):
                return (True, user[0])
            else:
                errors.append(("Wrong Email or Password!"))
        else:
            errors.append(("Wrong Email or Password!!"))
        return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

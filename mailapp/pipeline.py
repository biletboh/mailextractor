from .models import User, UserProfile
from django.contrib.auth import login

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        email = response['emails'][0]['value']
        username = email[:-10]

        # create a new social user 
        user, created = User.objects.get_or_create(username=username)

        user.email = email
        user.first_name = response['name']['givenName']
        user.last_name = response['name']['familyName']
        user.save()

        # create a profile for a new social user
        userprofile, created = UserProfile.objects.get_or_create(user=user)

        userprofile.gender = response['gender'] 
        userprofile.image_url = response['image']['url'] 
        userprofile.save()
        return {'user': user}

#def login_user(backend, reqest, user):
#    return login(request, user)


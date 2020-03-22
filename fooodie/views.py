from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from fooodie.models import Photo, UserProfile
from fooodie.forms import UserForm, UserProfileForm
import os, random


def home(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
##    #Ordering all photos randomly, picking first two
##    pics_to_choose = Photo.objects.order_by(?)[:1]
##    context_dict['pics_to_choose'] = pics_to_choose
##
##    #Will change this to use the same QuerySet eventually, to avoid double
##    #search and having the same picture be both a voting pic and random pic
##    random_pics = Photo.objects.order_by(?)[:3]
##    context_dict['random_pics'] = random_pics

    #Above will definitely work, this SHOULD work

    pics = Photo.objects.order_by('?')

    pics_to_choose = pics[:2]

    photo1=pics_to_choose.first()
    context_dict['photo1']=photo1

    photo2=pics_to_choose[1]
    context_dict['photo2']=photo2

    context_dict['pics_to_choose'] = pics_to_choose

    random_pics = pics[:4]
    context_dict['random_pics'] = random_pics

    response = render(request, 'fooodie/home.html', context = context_dict)
    return(response)

def about(request):
    context_dict = {}
    context_dict['userProfiles']
    response = render(request, 'fooodie/about.html')
    return(response)

def leaderboard(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    top_pics = Photo.objects.order_by('-votes')[:3] #Top 3
    context_dict['top_pics'] = top_pics

    top_profiles = UserProfile.objects.order_by('-totalVotes')[:8] #Top 8
    context_dict['top_profiles'] = top_profiles

    response = render(request, 'fooodie/leaderboard.html', context = context_dict)
    return(response)

#This will simply display the forms; the associated template will call
#one of the functions below dependent on button clicked
def user_signup_login(request):
    registered = False
    user_form = UserForm()
    profile_form = UserProfileForm()

    return render(request, 'fooodie/loginregister.html', context = {'user_form' : user_form,
                                                               'profile_form' : profile_form,
                                                               'registered' : registered})
##    context_dict = {}
##    context_dict['userProfiles']=UserProfile.objects.all()
##
##    response = render(request, 'fooodie/home.html')
##    return response

#Will focus on the registration/login logic first, implement into a single view later
def user_login(request):
    if request.method == 'POST':
        #Need to consider allowing email OR username potentially
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                print("Login success!")
                print("Is user thenticated?")
                print(user.is_authenticated)
                return redirect(reverse('fooodie:home'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'fooodie/loginregister.html')

#Will focus on the registration/login logic first, implement into a single view later
def register(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            #print('user id: '+str(user.id))

            #Creating the user's folder so we can put the profile pic into it
##            folder_path = os.path.join(settings.MEDIA_DIR, str(user.id))
##            os.mkdir(folder_path)
##
##            print('folder path: '+folder_path)
##
##            folder_path_str = str(folder_path)

            ##Think about placing the photo in the directory THEN just linking to that
            ##photo, like profile.picture = path_to_file

##            if 'picture' in request.FILES:
##                pro_pic = request.FILES['picture']
##                pro_pic2 = Image.open(pro_pic)
##                pro_pic2.filename = str(user.id)+'.jpg'
##                print('filename: '+pro_pic2.filename)
##                #filename = pro_pic.filename
##                pro_pic2.save(folder_path)

            #profile = UserProfile(user = user, slug = user.username)
##            profile_pic = request.FILES['picture']
##            path = default_storage.save(folder_path+'\\image.jpeg', ContentFile(profile_pic.read()))
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.slug = user.username
            #profile.picture = path

            profile.save()

            profile_pic_path = os.path.join(settings.MEDIA_DIR, str(profile.id))
            os.mkdir(profile_pic_path)

            if 'picture' in request.FILES:
                profile_pic = request.FILES['picture']
                extension = profile_pic.name.split('.')[-1] #Gets the string after the last period, to deal with name.txt.jpg situations
                path_to_pic = default_storage.save(profile_pic_path+'\\'+str(profile.id)+'_propic.'+extension, ContentFile(profile_pic.read()))
                profile.picture = path_to_pic
                profile.save()

            print('So USER id is '+str(user.id)+' and PROFILE id is '+str(profile.id)+' and picture is '+str(profile.picture))


            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'fooodie/loginregister.html', context = {'user_form' : user_form,
                                                               'profile_form' : profile_form,
                                                               'registered' : registered})

@login_required
def user_logout(request):
    logout(request) # Since we know the user is logged in, we can now just log them out.
    return redirect(reverse('fooodie:home'))

# May need to use multiple views for profiles; will try
# to figure out if view can used for both myprofile
# and other user profiles
def user_profile(request, user_profile_slug):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user
    context_dict = {}
    try:
        profile = UserProfile.objects.get(slug = user_profile_slug)
        context_dict['profile'] = profile
        photos = Photo.objects.filter(user = profile) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
        context_dict['photos'] = photos
    except:
        pass
    return render(request, 'fooodie/userprofile.html', context = context_dict)

def add_food_photo(request):
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    response=render(request, 'fooodie/uploadfoodphoto.html')

@login_required
def myprofile(request): #User's manage account site
    context_dict = {}
    context_dict['userProfiles']=UserProfile.objects.all()
    user = request.user

    search_term = ''

    try:
        profile = UserProfile.objects.get(user = user)
        context_dict['profile'] = profile
        photos = Photo.objects.filter(user__id = profile.id) #Get all the pictures with user_id. Useful documentation of this notation (user__id with two underscores)
        context_dict['photos'] = photos
    except:
        pass
    context_dict['user'] = user

    if 'search' in request.GET:
        search_term = request.GET['search']
        #fooodie = fooodie.filter(text__icontains=search_term)

    context={'search_terms':search_term}

    response = render(request, 'fooodie/myprofile.html', context = context_dict)
    return response
# Create your views here.

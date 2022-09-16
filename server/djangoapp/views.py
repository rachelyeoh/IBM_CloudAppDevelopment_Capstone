from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
         # If user exist and is valid, proceeed with login
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
         # otherwise display message invalid username or password and redirect back to login page
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Logging out of `{}`...".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        # url = "https://us-south.functions.appdomain.cloud/api/v1/web/yeohrachel%40gmail.com_dev/dealership-package/get_dealership.json"
        # # Get dealers from the URL
        # dealerships = get_dealers_from_cf(url)
        # # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # context["dealership_list"] = dealerships
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # url = "https://us-south.functions.appdomain.cloud/api/v1/web/yeohrachel%40gmail.com_dev/dealership-package/get-review"
        # result = get_dealer_reviews_from_cf(url, dealer_id=dealer_id)
        # context['reviews'] = result["reviews"]
        # context['dealership_name'] = result["dealership_name"]
        context['dealer_id'] = dealer_id
        return render(request, 'djangoapp/dealer_details.html', context)     


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    context['dealer_id'] = dealer_id
    if request.method == 'GET':
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context['cars'] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect("djangoapp:add_review", dealer_id=dealer_id)
        else:
            car = CarModel.objects.get(pk=request.POST['car'])
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            review["purchase_date"] = request.POST['purchasedate']
            review["purchase"] = request.POST['purchasecheck']
            review["name"] = request.user.first_name+" "+request.user.last_name
            review["car_make"] = car.name
            review["car_model"] = car.carmake.name
            review["car_year"] = car.year.strftime('%Y')
            json_payload = dict()
            json_payload["review"] = review
            # url = "https://us-south.functions.appdomain.cloud/api/v1/web/yeohrachel%40gmail.com_dev/dealership-package/post-review"
            # post_request(url, json_payload)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id) 

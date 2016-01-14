from django.shortcuts import render
# from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import re  # allows use of regex
from bike_app.models import Bike
import csv  # Allows reading CSV file into database
# import tablib
# import os


# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def form_page(request):

    return render(request, 'form.html')


def submit_response(request):
    selected_choice = request.POST['bikes']
    selected_use = request.POST['bikeUse']
    # selected_range = request.POST['bikeRange']
    # selected_speed = request.POST['bikeSpeed']
    if len(re.findall(r'\d+', selected_choice)) == 2:  # user selects price range
        lower_val = (re.findall(r'\d+', selected_choice))[0]
        upper_val = (re.findall(r'\d+', selected_choice))[1]
    else:  # In case user selects a price of > 4500.
        lower_val = (re.findall(r'\d+', selected_choice))[0]
        upper_val = "10000"

    bikes = Bike.objects.filter(price__gte=lower_val).filter(price__lt=upper_val).filter(best_use__icontains=selected_use)  # returns list of Bike objects

    # print("***** bikes:bikes is: ", {'bikes': bikes})
    for bike in bikes:
        print("***** bike.model is: ", bike.price)
    return render(request, 'results.html', {'bikes': bikes})
    # return HttpResponseRedirect(reverse('results'))


def bike_details(request):
    # bikes = Bike.objects.all()  # returns list of Bike objects
    # selected_choice = request.POST['bikes']
    # print("selected choice in bike_details is "), selected_choice
    # selected_use = request.POST['bikeUse']
    # bikey = request.session.get('url')
    # print("!!! Bike Model: ", bike_model)
    # print("!!! Bikey: ", bikey)
    # bike_model = request.get("bike_model")
    # print("bike_model is: ", bike_model)
    bike_model = request.POST['bike_model']
    print("!!! Bike Model:  ", bike_model)
    bikes = Bike.objects.filter(model__icontains='Faraday')  # returns list of Bike objects
    for bike in bikes:
        print("***** bike.model in views.bike_deails is: ", bike.model)
    return render(request, 'bike_details.html', {'bikes': bikes})

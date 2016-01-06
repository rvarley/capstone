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

    #  The following populates the Bike database with values in output.txt file.
    #  Uncomment to populate database with bike models
    """
    with open('output.txt', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            for i, field in enumerate(row):
                b = Bike(model=row[i])
                b.save()

    # bike_ = Bike.objects.all()  # returns list of Bike objects
    # [x[1] for x in bike_.values_list()]  #Returns list of all bike models in table
    """

    return render(request, 'form.html')


def submit_response(request):
    # bikes = Bike.objects.all()  # returns list of Bike objects
    selected_choice = request.POST['bikes']
    selected_use = request.POST['bikeUse']
    selected_range = request.POST['bikeRange']
    selected_speed = request.POST['bikeSpeed']
    if len(re.findall(r'\d+', selected_choice)) == 2:  # user selects price range
        lower_val = (re.findall(r'\d+', selected_choice))[0]
        upper_val = (re.findall(r'\d+', selected_choice))[1]
    else:  # In case user selects a price of > 4500.
        lower_val = (re.findall(r'\d+', selected_choice))[0]
        upper_val = "10000"

    bikes = Bike.objects.filter(price__gte=lower_val).filter(price__lt=upper_val).filter(best_use__icontains=selected_use)  # returns list of Bike objects
    # print("***** selected_range is: ", selected_range)
    # print("***** selected_speed is: ", selected_speed)
    # print("***** selected_use is: ", selected_use)
    # print("***** bikes:bikes is: ", {'bikes': bikes})
    for bike in bikes:
        print("***** bike.model is: ", bike.price)
    return render(request, 'results.html', {'bikes': bikes})
    # return HttpResponseRedirect(reverse('results'))

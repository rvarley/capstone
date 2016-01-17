from django.shortcuts import render
import re  # allows use of regex
from bike_app.models import Bike


def home_page(request):
    return render(request, 'home.html')


def form_page(request):

    return render(request, 'form.html')


def submit_response(request):
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

    bikes = Bike.objects.filter(price__gte=lower_val)\
        .filter(price__lte=upper_val).filter(best_use__icontains=selected_use)\
        .filter(top_speed__gte=selected_speed)\
        .filter(b_range__gte=selected_range)  # returns list of Bike objects

    print("***** selected_use is:", selected_use)
    print("***** lower val {}: ".format(lower_val))
    print("***** upper val {}: ".format(upper_val))
    print("***** selected_range {}: ".format(selected_range))
    print("***** Type, selected_range is: ", type(selected_range))
    # for bike in bikes:
    #     print("***** bike.model is:", bike.model)
    return render(request, 'results.html', {'bikes': bikes})


def bike_details(request):

    bike_model = request.POST['bike_model']
    print("!!! Bike Model:  ", bike_model)
    bikes = Bike.objects.filter(model__icontains=bike_model)  # returns list of Bike objects
    print("***** bikes type in views.bike_details is: ", type(bikes))
    return render(request, 'bike_details.html', {'bikes': bikes})

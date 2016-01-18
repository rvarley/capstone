from django.shortcuts import render
import re  # allows use of regex
from bike_app.models import Bike


def home_page(request):
    """
    Renders the home page.
    home variable used so base.html template knows what to display
    when inherited by the home.html template.
    """

    home = {"home": "home"}
    return render(request, 'home.html', {'home': home})


def form_page(request):
    """
    Renders the form.html template.  The user enters query selections
    from the form page.
    """

    return render(request, 'form.html')


def submit_response(request):
    """
    Queries database for bikes matching user's selection criteria.
    Renders a list of bikes that meet user's selection criteria.

    Inputs - selection criteria entered by the user on the forms page
    Output - A list of bike objects
    """

    selected_choice = request.POST['bikes']
    selected_use = request.POST['bikeUse']
    selected_range = request.POST['bikeRange']
    selected_speed = request.POST['bikeSpeed']
    if len(re.findall(r'\d+', selected_choice)) == 2:  # user selects a range
                                                       # of prices
        lower_val = (re.findall(r'\d+', selected_choice))[0]
        upper_val = (re.findall(r'\d+', selected_choice))[1]
    else:  # In case user selects a price of > 4500 (single price vs. range)
        lower_val = (re.findall(r'\d+', selected_choice))[0]
        upper_val = "10000"

    results = Bike.objects.filter(price__gte=lower_val)\
        .filter(price__lte=upper_val).filter(best_use__icontains=selected_use)\
        .filter(top_speed__gte=selected_speed)\
        .filter(b_range__gte=selected_range)  # returns list of Bike objects

    return render(request, 'results.html', {'results': results})


def bike_details(request):
    """
    Queries database for details on specified bike model and
    renders details on a specific bike.

    Input - A bike model
    Output - A bike object containing details on the selected bike model
    """

    bike_model = request.POST['bike_model']
    bikes = Bike.objects.filter(model__icontains=bike_model)  # returns list
                                                              # of Bike objects

    return render(request, 'bike_details.html', {'bikes': bikes})

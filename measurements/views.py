from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
# https://pypi.org/project/geopy/
# https://pypi.org/project/geoip2/
from geopy.geocoders import Photon
# For calculating distance between two variables
from geopy.distance import geodesic
from .utils import get_geo


# Create your views here.


def calculate_distance_view(request):
    obj = get_object_or_404(Measurement, id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Photon(user_agent="measurements")

    ip = '72.14.207.99'
    country, city, lat, lon = get_geo(ip)
    # print('location country', country)
    # print('location city', city)
    # print('location lat, lon', lat, lon)

    location = geolocator.geocode(city)
    # print('###', location)

    l_lat = lat
    l_lon = lon
    pointA = (l_lat, l_lon)

    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        # print(destination)
        # print(destination.latitude)
        # print(destination.longitude)
        d_lat = destination.latitude
        d_lon = destination.longitude

        pointB = (d_lat, d_lon)

        distance = round(geodesic(pointA, pointB).km, 2)

        instance.location = location
        instance.distance = distance
        # instance.location = 'San Francisco'
        # instance.distance = 5000.00
        instance.save()

    context = {
        'distance': obj,
        'form': form,
    }

    return render(request, 'measurements/main.html', context)

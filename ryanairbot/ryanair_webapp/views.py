from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import UserForm
from django.conf import settings as django_settings

import json
import requests
from collections import namedtuple

# Create your views here.

def main(request):
    user_form = UserForm()
    return render(request,
                  "index.html",
                  {"form": user_form})

def return_flights(request):

    if request.method == "GET":
        return HttpResponseRedirect(reverse("main"))

    if request.method == "POST":
        form_data = UserForm(request.POST)
        print(form_data.errors)

        if form_data.is_valid():
            origin_city = form_data.cleaned_data["origin_city"]
            arrival_city = form_data.cleaned_data["arrival_city"]
            search_start_date = form_data.cleaned_data["search_start_date"]
            search_end_date = form_data.cleaned_data["search_end_date"]

            res = [origin_city, arrival_city, str(search_start_date), str(search_end_date)]
            print(
                origin_city,
                arrival_city,
                search_start_date,
                search_end_date
            )

            airports_json_file = open(django_settings.RYANAIR_AIRPORTS_ROOT)
            airports = json.load(airports_json_file)

            done_flag = 0
            for a in airports:
                if done_flag == 2:
                    break

                if a["name"] == origin_city:
                    origin_city_dict = a
                    done_flag += 1

                if a["name"] == arrival_city:
                    arrival_city_dict = a
                    done_flag += 1

            print(origin_city_dict["code"])
            print(arrival_city_dict["code"])
            fares = requests.get("https://www.ryanair.com/api/farfnd/v4/oneWayFares/" + origin_city_dict["code"] + "/" + arrival_city_dict["code"] + "/cheapestPerDay?outboundMonthOfDate=2023-09-01&currency=PLN").json()

            prices = []

            the_cheapest_flight = {'price': {'value': 1311.13 }}
            for f in fares["outbound"]["fares"]:
                if f["unavailable"] == False:
                    prices.append(f)
                    if f["price"]["value"] < the_cheapest_flight["price"]["value"]:
                        the_cheapest_flight = f

            return render(request,
                          "results.html",
                          {
                              "all_prices": prices,
                              "cheapest_flight": the_cheapest_flight})

        else:
            print(form_data.errors)
            return HttpResponse(form_data.errors)




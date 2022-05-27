from urllib.error import HTTPError
from datetime import datetime, timedelta
from main import User
import requests
day_of_week = datetime.today().weekday()
print(day_of_week)

LOCATION_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
FLIGHT_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
API_KEY = "Xr_BF4Uyg4T9g8Hiv75bVXbulMuIca9w"
headers = {
    "apikey": API_KEY
        }


def look_for_flights(user_prefs, destination):
    if user_prefs["specific_search_start_date"]:
        print(user_prefs["specific_search_start_date"])
        print(today)
        start_date = (today + timedelta(days=20)).strftime("%d/%m/%Y")
        end_date = (today + timedelta(days=50)).strftime("%d/%m/%Y")
        print(start_date)
    flight_parameters = {
        "fly_from": destination["home_airport"],
        "fly_to": destination["iata"],
        "date_from": (today + timedelta(days=int(user_prefs['search_start_date']))).strftime("%d/%m/%Y"),
        "date_to": (today + timedelta(days=int(user_prefs['search_length']))).strftime("%d/%m/%Y"),
        "nights_in_dst_from": user_prefs["min_nights"],
        "nights_in_dst_to": user_prefs["max_nights"],
        "flight_type": "round",
        "adults": user_prefs["num_adults"],
        "children": user_prefs["num_children"],
        "infants": user_prefs["num_infants"],
        "curr": user_prefs["currency"],
        "selected_cabins": user_prefs["cabin_class"],
        "max_fly_duration": user_prefs["max_flight_time"],
        "max_sector_stopovers": user_prefs["max_stops"],
        "limit": 500
    }
    try:
        search_response = requests.get(url=FLIGHT_ENDPOINT, headers=headers, params=flight_parameters)
        # search_response.raise_for_status()
    except HTTPError:
        print("Home airport code is messed up")
        return
    else:
        return search_response.json()


def process_flight_info(flight_data):
        data = flight_data["data"][0]
        flight_data_dict = \
            {
                'city_from': data['cityFrom'],
                'city_from_code': data['cityCodeFrom'],
                'city_to': data['cityTo'],
                'city_to_code': data['cityCodeTo'],
                'departure': data['local_departure'].split("T")[0],
                'leave_destination_date': data["route"][-1]['local_departure'].split("T")[0],
                'arrival': data["route"][-1]['local_arrival'].split("T")[0],
                'nights_at_destination': int(data['nightsInDest']) + 1,
                'price': data['price']
            }
        return flight_data_dict


def send_email(user_name, user_email, flight_deal_list):
    url = "https://api.sendinblue.com/v3/smtp/email"
    payload = {
            "sender": {
                "email": "flightclubdeals@gmail.com",
                "name": "Flight Club"
            },
            "to": [{
                "email": user_email,
                "name": user_name
            }],
            "subject": "This week's dose of flight deals is here!",
            "params": {
                "destinations": flight_deal_list
            },
            "templateId": 1
        }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": "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"
    }
    response = requests.post(url, json=payload, headers=headers)
    print("Response Text")
    print(response.text)
    print("\nEnd of CODE")
    return


# Scheduler runs everyday, this turns it into a weekly task run on Friday (day 4)
if day_of_week == 4:
    today = datetime.now()
    print(today)
    tomorrow = (today + timedelta(days=1))
    if tomorrow > today:
        print("Greater")
    # Grab data from database
    all_users = User.query.all()
    print(all_users)
    for u in all_users:
        flight_deal_list = []
        user_name = u.name
        user_email = u.email
        print(f"{user_name}: {user_email}")

        user_preferences_dict = u.preferences[0].__dict__
        user_destinations_dict = u.destinations[0].__dict__
        print("\n\n")
        print(f'Preferences: {user_preferences_dict}')
        print(f'Destinations: {user_destinations_dict}')
        print("\n\n")

        passengers = ""
        if user_preferences_dict['num_adults'] != 0:
            passengers += f"{user_preferences_dict['num_adults']} adults"
        if user_preferences_dict['num_children'] != 0:
            passengers += f", {user_preferences_dict['num_children']} children"
        if user_preferences_dict['num_infants'] != 0:
            passengers += f", {user_preferences_dict['num_infants']} infants"
        print(passengers)
        list_of_dicts = []
        for x in range(1, 11):
            dict_to_add = {"iata": user_destinations_dict[f'city{x}'],
                           "price_ceiling": user_destinations_dict[f'price{x}'],
                           "home_airport": user_destinations_dict["home_airport"]}
            if dict_to_add["iata"] is None:
                pass
            else:
                list_of_dicts.append(dict_to_add)
        print("\n\n")
        print("List of Destination Dictionaries")
        print(list_of_dicts)
        print("\n\n")
        for destination in list_of_dicts:

            print("\n\n")
            print("Destination")
            print(destination)
            flight_data = look_for_flights(user_prefs=user_preferences_dict, destination=destination)
            # print(flight_data)
            if len(flight_data["data"]) == 0:
                print(f"No flight data for destination: {destination['iata']}")
                continue
            else:
                flight_dict = process_flight_info(flight_data=flight_data)
                print("\n\n")
                print("Flight Data for Destination")
                print(flight_dict)
                flight_deal_list.append(
                    {
                        "city": flight_dict["city_to"],
                         "price": flight_dict["price"],
                         "nights": flight_dict["nights_at_destination"],
                         "date1": flight_dict["departure"],
                         "date2": flight_dict["arrival"],
                         "image": "REPLACE LATER",
                         "passengers": passengers,
                         "link": f"https://www.kiwi.com/en/search/results/{flight_dict['city_from_code']}/"
                                 f"{flight_dict['city_to_code']}/{flight_dict['departure']}/"
                                 f"{flight_dict['leave_destination_date']}?sortBy=price"
                    }
                )

        if flight_deal_list:
            send_email(user_name=user_name, user_email=user_email, flight_deal_list=flight_deal_list)
            print("\n\n\n")
            print("Flight Deal List:")
            print(flight_deal_list)
        else:
            print("No flight deals this time around :(")





    # ------------------------







else:
    print("Not Flight Deal time yet!")
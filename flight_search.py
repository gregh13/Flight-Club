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


def search_destination_code(user_city):
    location_query = {
                "term": user_city,
                "location_types": "city",
                "limit": 1,
                "active_only": "true",
            }
    response = requests.get(url=LOCATION_ENDPOINT, headers=headers, params=location_query)
    code_data = response.json()
    try:
        iata_code = code_data["locations"][0]["code"]
    except IndexError:
        print(f"ERROR! {user_city} didn't get any results. Check spelling?")
        iata_code = "WTF"
        return iata_code
    else:
        return iata_code


def look_for_flights(user_prefs, user_dest):
    if user_prefs["specific_search_start_date"]:
        print(user_prefs["specific_search_start_date"])
        print(today)
        start_date = (today + timedelta(days=20)).strftime("%d/%m/%Y")
        end_date = (today + timedelta(days=50)).strftime("%d/%m/%Y")
        print(start_date)
    flight_parameters = {
        "fly_from": user_dest["home_airport"],
        "fly_to": user_dest["iata_code"],
        "date_from": (today + timedelta(days=int(user_prefs['search_start_date']))).strftime("%d/%m/%Y"),
        "date_to": (today + timedelta(days=int(user_prefs['search_length']))).strftime("%d/%m/%Y"),
        "nights_in_dst_from": user_prefs["min_nights"],
        "nights_in_dst_to": user_prefs["max_nights"],
        "flight_type": user_prefs["flight_type"],
        "adults": user_prefs["num_adults"],
        "children": user_prefs["num_children"],
        "infants": user_prefs["num_infants"],
        "curr": user_prefs["currency"],
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
        city_from = data['cityFrom']
        city_from_code = data['cityCodeFrom']
        city_to = data['cityTo']
        city_to_code = data['cityCodeTo']
        departure = data['local_departure'].split("T")[0]
        leave_destination_date = data["route"][-1]['local_departure'].split("T")[0]
        arrival = data["route"][-1]['local_arrival'].split("T")[0]
        nights_at_destination = int(data['nightsInDest']) + 1
        price = data['price']
        return [city_from, city_from_code, city_to, city_to_code, departure, leave_destination_date, arrival, nights_at_destination, price]

# Scheduler runs everyday, this turns it into a weekly task run on Friday (day 4)
if day_of_week == 1:
    today = datetime.now()
    print(today)
    tomorrow = (today + timedelta(days=1))
    if tomorrow > today:
        print("Greater")
    # Grab data from database
    all_users = User.query.all()
    print(all_users)
    for u in all_users:
        user_name = u.name
        user_email = u.email
        user_preferences_dict = u.preferences[0].__dict__
        user_destinations_dict = u.destinations[0].__dict__
        # print(f'Preferences: {user_preferences_dict}')
        # print(f'Destinations: {user_destinations_dict}')
        list_of_dicts = []
        for x in range(1, 11):
            dict_to_add = {"city": user_destinations_dict[f'city{x}'],
                           "price_ceiling": user_destinations_dict[f'price{x}'],
                           "home_airport": user_destinations_dict["home_airport"]}
            if dict_to_add["city"] is None:
                pass
            else:
                list_of_dicts.append(dict_to_add)
        # print(list_of_dicts)
        for destination in list_of_dicts:
            city = destination["city"]
            iata_code = search_destination_code(user_city=city)
            destination["iata_code"] = iata_code
            print(destination)
            flight_data = look_for_flights(user_prefs=user_preferences_dict, user_dest=destination)
            clean_data_list = process_flight_info(flight_data=flight_data)
            print(clean_data_list)



    # ------------------------







else:
    print("Not Flight Deal time yet!")
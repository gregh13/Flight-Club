from urllib.error import HTTPError
from datetime import datetime, timedelta, date
from main import User, Preferences, db
from iata_codes import all_cities_international
import requests
import base64
import urllib.parse
import random

day_of_week = datetime.today().weekday()

LOCATION_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
FLIGHT_ENDPOINT = "https://tequila-api.kiwi.com/v2/search"
FLIGHT_API_KEY = "Xr_BF4Uyg4T9g8Hiv75bVXbulMuIca9w"

GOAT_ACCESS_KEY = "e1d1a17cc2722373422ab8cbd9ec51ef"
GOAT_SECRET_KEY = "ab3b07cb5f9b54eb249b495d6da62e67"
headers = {
    "apikey": FLIGHT_API_KEY
        }


def figure_out_dates(user_prefs):
    today = date.today()
    start_specific = user_prefs["specific_search_start_date"]
    end_specific = user_prefs["specific_search_end_date"]
    forward_start = (today + timedelta(days=user_prefs["search_start_date"])).strftime("%d/%m/%Y")
    forward_end = (today + timedelta(days=(user_prefs["search_start_date"] +
                                           user_prefs["search_length"]))).strftime("%d/%m/%Y")
    # Sets defaults, helps clean up 'if' statements below
    date_from = forward_start
    date_to = forward_end

    if start_specific:
        if end_specific:
            if start_specific >= today:
                # Start date is ok (and end date since validated with form)
                # Kiwi Flight Search requires dd/mm/yyyy format
                date_from = start_specific.strftime("%d/%m/%Y")
                date_to = end_specific.strftime("%d/%m/%Y")

            elif end_specific > (today + timedelta(days=(1 + user_prefs["min_nights"]))):
                # start date is past, check end date is ok
                date_from = today.strftime("%d/%m/%Y")
                date_to = end_specific.strftime("%d/%m/%Y")

        elif start_specific >= today:
            # No end date, start date is okay (not past)
            date_from = start_specific.strftime("%d/%m/%Y")

    elif end_specific:
        # Only end date, using default start advance
        if end_specific > (today + timedelta(days=(1 + user_prefs["min_nights"] + user_prefs["search_start_date"]))):
            # end date is okay (far enough out to possibly get results)
            date_to = end_specific.strftime("%d/%m/%Y")

    date_dictionary = {"date_from": date_from, "date_to": date_to}

    return date_dictionary


def road_goat_image_search(city_name, country_to):
    def send_api_request(query):
        url = f"https://api.roadgoat.com/api/v2/destinations/auto_complete?q={query}"
        encoded_bytes = base64.b64encode(f'{GOAT_ACCESS_KEY}:{GOAT_SECRET_KEY}'.encode("utf-8"))
        auth_key = str(encoded_bytes, "utf-8")
        headers = {
            'Authorization': f'Basic {auth_key}'
        }
        response = requests.get(url=url, headers=headers)
        res = response.json()
        print("\nAutocomplete Data Results:")
        print(res)
        return res

    print(f"\nCountry: {country_to}\n")
    print(f"City Name: {city_name}")
    city_name = city_name.split(" - ")[0]
    url_encoded_city_name = urllib.parse.quote(city_name)
    url_encoded_country_name = urllib.parse.quote(country_to)

    results = send_api_request(query=url_encoded_city_name)
    if results["data"]:
        if results['data'][0]['relationships']['featured_photo']['data']:
            print(results["included"])
            image_link = results["included"][0]["attributes"]["image"]["full"]
        else:
            results = send_api_request(query=url_encoded_country_name)
            if results["data"]:
                if results['data'][0]['relationships']['featured_photo']['data']:
                    print(results["included"])
                    image_link = results["included"][0]["attributes"]["image"]["full"]
                else:
                    airplane = "https://images.pexels.com/photos/46148/aircraft-jet-landing-cloud-46148.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
                    image_link = airplane
            else:
                airplane = "https://images.pexels.com/photos/46148/aircraft-jet-landing-cloud-46148.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
                image_link = airplane
    else:
        results = send_api_request(query=url_encoded_country_name)
        if results["data"]:
            if results['data'][0]['relationships']['featured_photo']['data']:
                print(results["included"])
                image_link = results["included"][0]["attributes"]["image"]["full"]
            else:
                airplane = "https://images.pexels.com/photos/46148/aircraft-jet-landing-cloud-46148.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
                image_link = airplane
        else:
            airplane = "https://images.pexels.com/photos/46148/aircraft-jet-landing-cloud-46148.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
            image_link = airplane



    print("IMAGE LINK:")
    print(image_link)
    print("END OF LINK")

    return image_link


def look_for_flights(user_prefs, destination):

    flight_date_dict = figure_out_dates(user_prefs)
    # print(flight_date_dict)
    # print(type(flight_date_dict["date_to"]))
    # print(user_prefs)
    # print(destination)
    flight_parameters = {
        "fly_from": destination["home_airport"],
        "fly_to": destination["iata"],
        "date_from": flight_date_dict["date_from"],
        "date_to": flight_date_dict["date_to"],
        "nights_in_dst_from": user_prefs["min_nights"],
        "nights_in_dst_to": user_prefs["max_nights"],
        "flight_type": "round",
        "adults": user_prefs["num_adults"],
        "children": user_prefs["num_children"],
        "infants": user_prefs["num_infants"],
        "curr": destination["currency"],
        "selected_cabins": user_prefs["cabin_class"],
        "max_fly_duration": user_prefs["max_flight_time"],
        "max_sector_stopovers": user_prefs["max_stops"],
        "limit": 22
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
                'country_to': data['countryTo']['name'],
                'departure': data['local_departure'].split("T")[0],
                'leave_destination_date': data["route"][-1]['local_departure'].split("T")[0],
                'arrival': data["route"][-1]['local_arrival'].split("T")[0],
                'nights_at_destination': int(data['nightsInDest']) + 1,
                'price': data['price']
            }
        return flight_data_dict


def send_email(user_name, user_email, flight_deal_list, template_id):
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
            "subject": "The results for your flight search are here! Come check it out",
            "params": {
                "destinations": flight_deal_list
            },
            "templateId": template_id
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


# Grab data from database
all_users = User.query.all()
print(all_users)
for u in all_users:
    print(u.name)
    email_day = u.preferences[0].email_day
    if day_of_week != email_day:
        print("Not today, my friend!")
        continue
    print("TODAY IS THE DAY!")
    user_preference_object = Preferences.query.filter_by(user_pref_id=u.preferences[0].user_pref_id).first()
    email_freq = user_preference_object.email_frequency
    # Find User Pref instead!!
    if email_freq != 1:
        if email_freq == 2:
            print("Biweekly, send")
            user_preference_object.email_frequency = 3
            db.session.commit()
        elif email_freq == 3:
            print("Biweekly, don't send")
            user_preference_object.email_frequency = 2
            db.session.commit()
            continue
        elif email_freq == 4:
            print("Monthly, send")
            user_preference_object.email_frequency = 5
            db.session.commit()
        elif email_freq == 5 or email_freq == 6:
            print("Monthly, don't send")
            user_preference_object.email_frequency = (email_freq + 1)
            db.session.commit()
            continue
        elif email_freq == 7:
            print("Monthly, don't send")
            user_preference_object.email_frequency = 4
            db.session.commit()
            continue

    flight_deal_list = []
    user_name = u.name
    user_email = u.email
    print(f"{user_name}: {user_email}")

    user_preferences_dict = u.preferences[0].__dict__
    user_destinations_dict = u.destinations[0].__dict__
    # print("\n")
    # print(f'Preferences: {user_preferences_dict}')
    # print(f'Destinations: {user_destinations_dict}')
    # print("\n")
    total_passengers = (user_preferences_dict['num_adults']
                        + user_preferences_dict['num_children']
                        + user_preferences_dict['num_infants'])
    passengers = ""
    if user_preferences_dict['num_adults'] != 0:
        if user_preferences_dict['num_adults'] == 1:
            passengers += f"{user_preferences_dict['num_adults']} Adult"
        else:
            passengers += f"{user_preferences_dict['num_adults']} Adults"
    if user_preferences_dict['num_children'] != 0:
        if user_preferences_dict['num_children'] == 1:
            passengers += f"{user_preferences_dict['num_children']} Child"
        else:
            passengers += f", {user_preferences_dict['num_children']} Children"
    if user_preferences_dict['num_infants'] != 0:
        if user_preferences_dict['num_infants'] == 1:
            passengers += f"{user_preferences_dict['num_infants']} Infant"
        else:
            passengers += f", {user_preferences_dict['num_infants']} Infants"
    # print(passengers)
    list_of_dicts = []
    for x in range(1, 11):
        dict_to_add = {"iata": user_destinations_dict[f'city{x}'],
                       "price_ceiling": user_destinations_dict[f'price{x}'],
                       "home_airport": user_destinations_dict["home_airport"],
                       "currency": user_destinations_dict["currency"]}
        if dict_to_add["iata"] is None:
            pass
        else:
            list_of_dicts.append(dict_to_add)
    # print("\n")
    # print("List of Destination Dictionaries")
    # print(list_of_dicts)
    # print("\n")
    bad_codes = []
    for destination in list_of_dicts:
        # print("\n")
        # print("Destination")
        # print(destination)
        # 'Surprise Me' choice
        if destination["iata"] == "???":
            # Protects against randomly getting "???" again
            while destination["iata"] == "???":
                destination["iata"] = random.choice(list(all_cities_international))
                print("SURPRISE MEEEEE")
                print(destination["iata"])
# -----------------------------------------------------------
#         for code in list(all_cities_international):
#             print(code)
#             destination["iata"] = code
#             flight_data = look_for_flights(user_prefs=user_preferences_dict, destination=destination)
#             # print(flight_data)
#             # When fly_to location code is bad or doesn't exist
#             if 'Unprocessable Entity' in flight_data.values():
#                 print("BAD AIRPORT CODE\n")
#                 bad_codes.append(destination["iata"])
#                 print(bad_codes)
#                 continue
#
#         print(f"\n\nBAD CODES:\n{bad_codes}")
#         break

        bad_boys = ['GON', 'BEO', 'RPM', 'NIC', 'NDZ', 'NCA',
                    'NUB', 'NYN', 'OBD', 'OKQ', 'OSK', 'OTU',
                    'PCH', 'AOL', 'PZE', 'PMQ', 'PMG', 'PRQ',
                    'PUD', 'RBP', 'RAT', 'RJN', 'RAM', 'RBJ',
                    'RIG', 'ROY', 'RNE', 'SZT', 'LTT', 'XPZ',
                    'OES', 'SVZ', 'ULA', 'SAI', 'NMG', 'STB',
                    'HEX', 'SWG', 'ZBY', 'QFK', 'ZEG', 'ZRI',
                    'SZM', 'HIL', 'JHQ', 'NKD', 'SOD', 'TZN',
                    'SOI', 'SQO', '???', 'TMH', 'TRA', 'TEU',
                    'TKB', 'TXM', 'TDB', 'TIS', 'TPR', 'TGN',
                    'TTS', 'TUR', 'TUJ', 'ULI', 'URU', 'USL',
                    'UTK', 'XVS', 'VCD', 'VLG', 'VME', 'VIV',
                    'VOH', 'VLK', 'WET', 'WBA', 'WGE', 'WKA',
                    'AGL', 'WSR', 'WED', 'WTO', 'WTE', 'WUD',
                    'WYN', 'KYX', 'UGU']






        for key in bad_boys:
            all_cities_international




# -------------------------------------------------------

        flight_data = look_for_flights(user_prefs=user_preferences_dict, destination=destination)
        # print(flight_data)
        # When fly_to location code is bad or doesn't exist
        if 'Unprocessable Entity' in flight_data.values():
            print("BAD AIRPORT CODE\n")
            bad_codes.append(destination["iata"])

            continue
        if len(flight_data["data"]) == 0:
            print(f"No flight data for destination: {destination['iata']}\n")
            bad_codes.append(destination["iata"])
            continue
        else:
            flight_dict = process_flight_info(flight_data=flight_data)
            # print("\n")
            # print("Flight Data for Destination")
            # print(flight_dict)
            # print("\n")
            # searched_currency = flight_data["currency"]
            # currency_rate_to_USD = flight_data["fx_rate"]
            price_ceiling = total_passengers * destination["price_ceiling"]

            if flight_dict["price"] <= price_ceiling:
                depart = datetime.strptime(flight_dict["departure"], '%Y-%m-%d')
                depart_day = depart.strftime('%A, %b %-d')
                back_home = datetime.strptime(flight_dict["arrival"], '%Y-%m-%d')
                back_home_day = back_home.strftime('%A, %b %-d')

                price_formatted = "{:,}".format(flight_dict["price"])
                print(price_formatted)
                price_formatted = str(price_formatted) + f" {destination['currency']}"
                print(price_formatted)
                city_name = all_cities_international[destination["iata"]]
                image_link = road_goat_image_search(city_name=city_name, country_to=flight_dict["country_to"])

                flight_deal_list.append(
                    {
                         "city": flight_dict["city_to"],
                         "price": price_formatted,
                         "nights": flight_dict["nights_at_destination"],
                         "date1": depart_day,
                         "date2": back_home_day,
                         "image": image_link,
                         "passengers": passengers,
                         "link": f"https://www.kiwi.com/en/search/results/{flight_dict['city_from_code']}/"
                                 f"{flight_dict['city_to_code']}/{flight_dict['departure']}/"
                                 f"{flight_dict['leave_destination_date']}?sortBy=price"
                    }
                )
            else:
                print("Price is NO GOOD\n")

    if flight_deal_list:
        template_id = 1
        send_email(user_name=user_name,
                   user_email=user_email,
                   flight_deal_list=flight_deal_list,
                   template_id=template_id)
        print("\n")
        print("Flight Deal List:")
        print(flight_deal_list)
    else:
        template_id = 3
        # send_email(user_name=user_name,
        #            user_email=user_email,
        #            flight_deal_list=flight_deal_list,
        #            template_id=template_id)
        print("\n\n")
        print("No flight deals this time around :(\n NO DEALSSS")
        print("\n\n")
        print(bad_codes)





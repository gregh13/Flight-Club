# List of airline codes/names to exclude if user chooses 'Exclude Bad Airlines'

bad_airline_dict = {
    "VH": "Viva Air Colombia",
    "VB": "VivaAerobus Mexican",
    "Y4": "Volaris Mexican",
    "FR": "Ryanair Irish",
    "RR": "Buzz (Ryanair)",
    "4O": "Interjet Mexican",
    "VY": "Vueling Airlines Spanish",
    "U2": "EasyJet UK",
    "DS": "EasyJet Switzerland",
    "PS": "Ukraine International Airlines",
    "TP": "TAP Air Portugal",
    "G3": "Gol Airlines Brazilian",
    "ET": "Ethiopian Airlines",
    "FI": "Iceland Air",
    "IW": "Wings Air (Lion Air) Indo",
    "JT": "Lion Air Indonesian",
    "SL": "Thai Lion Air",
    "TU": "Tunisair Tunisian",
    "ZI": "Aigle Azur French",
    "MT": "Thomas Cook UK",
    "WW": "WOW Air Iceland",
    "KU": "Kuwait",
    "PK": "Pakistan International Airlines",
    "AH": "Air Algerie",
    "DV": "Scat Kazakhstan",
    "PA": "Airblue Pakistan",
    "EP": "Iran Aseman Airlines",
    "RA": "Nepal Airlines",
    "MH": "Malaysia Airlines",
    "MU": "China Eastern",
    "TT": "Tiger Air Australia",
    "IT": "Tiger Air Taiwan",
    "PR": "Air Philippines",
    "CA": "Air China",
    "CU": "Cubana",
    "AI": "Air India",
    "IX": "Air India Express",
    "CG": "Airlines PNG",
    "QV": "Lao Airlines",
    "KM": "Air Malta",
    "JU": "Air Serbia",
    "JD": "Capital Airlines",
    "5J": "Cebu Pacific",
    "G5": "China Express Airlines",
    "TM": "LAM Mozambique",
    "8Q": "Onur Air",
    "NK": "Spirit",
    "RO": "TAROM",
    "8Z": "Wizz Air Hungary",
    "W6": "Wizz Air",
    "5W": "Wizz Air Abu Dhabi",
    "W9": "Wizz Air UK",
    "MF": "Xiamen Airlines",
    "3K": "Jetstar Singapore",
    "JQ": "Jetstar Singapore",
    "IB": "Iberia Airlines Spanish",
    "CI": "China Airlines",
    "FB": "Bulgaria Air",
    "HY": "Uzbekistan Airway",
    "F9": "Frontier Airlines"
}


string = ""

for airline in list(bad_airline_dict.keys()):
    string += airline
    if airline != list(bad_airline_dict.keys())[-1]:
        string += ","

bad_airline_string = string


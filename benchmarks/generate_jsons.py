import json
import random
import string
from datetime import datetime, timedelta

def generate_random_string(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_random_tournament_name():
    adjectives = ["Global", "International", "World", "Elite", "Premier", "Ultimate"]
    nouns = ["Cup", "League", "Championship", "Tournament", "Challenge"]
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    return f"{adjective} {noun}"

def generate_random_team_name():
    prefixes = ["FC", "AC", "United", "City", "Sporting", "Athletic"]
    suffixes = ["United", "City", "FC", "Rovers", "Wanderers", "Athletic"]
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    city = generate_random_string(random.randint(5, 10)).capitalize()
    return f"{prefix} {city} {suffix}"

tournaments = [generate_random_tournament_name() for _ in range(5)]
teams = set([generate_random_team_name() for _ in range(random.randint(2, 1000))])


start_dates = [datetime(2000, 1, 1), datetime(2030, 12, 31), datetime(2022, 9, 1), datetime(2024, 14, 3), datetime(2010, 10, 10)]
end_dates = [date + timedelta(days=270) for date in start_dates]

for i in range(5):
    tournament_name = tournaments[i]
    start_date = start_dates[i].strftime("%Y-%m-%d")
    end_date = end_dates[i].strftime("%Y-%m-%d")
    start_time = "18:00:00.000"
    end_time = "21:45:00.000"

    
    num_participants = random.randint(2,len(teams))  # Número aleatorio de participantes
    participants = random.sample(sorted(teams), num_participants)

    data = {
        "tournament_name": tournament_name,
        "start_date": start_date,
        "end_date": end_date,
        "start_time": start_time,
        "end_time": end_time,
        "participants": participants
    }

    json_data = json.dumps(data, indent=4)
    with open(f"{tournament_name}.json", "w") as file:
        file.write(json_data)
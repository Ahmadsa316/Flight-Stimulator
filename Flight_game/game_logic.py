from datetime import timedelta
from datetime import datetime
import random
from connect_database import connect_database
from math import radians, sin, cos, sqrt, atan2
import time
from hurdles import get_hurdles_for_level, level_hurdles


# Create a new user or retrieve an existing one
def get_or_create_user(cursor, username):
    cursor.execute("SELECT id, fuel_consumed FROM User WHERE username = %s", (username,))
    user = cursor.fetchone()
    if user:
        print(f"Welcome back, {username}! Resuming from where you left off.")
        return user
    else:
        cursor.execute("INSERT INTO User (username, fuel_consumed) VALUES (%s, NULL)", (username,))
        print(f"Welcome {username}. Thank you Registering, Dive into the Fun World. Where dream become reality!!!")
        return cursor.lastrowid, None

# Fetch available airports based on both the continent and country
def get_airports_for_country_and_continent(cursor, country, continent):
    cursor.execute("""
        SELECT a.id, a.name, a.latitude_deg, a.longitude_deg 
        FROM Airport a
        JOIN Country c ON a.iso_country = c.id
        WHERE a.iso_country = %s 
          AND c.continent = %s
        LIMIT 12  -- Limit to 12 airports
    """, (country, continent))
    airports = cursor.fetchall()
    return airports

# Insert flight details
def create_flight(cursor, departure_airport_id, arrival_airport_id, departure_time, arrival_time):
    cursor.execute("""
        INSERT INTO Flight (departure_airport_id, arrival_airport_id, scheduled_departure_time, scheduled_arrival_time)
        VALUES (%s, %s, %s, %s)
    """, (departure_airport_id, arrival_airport_id, departure_time, arrival_time))
    return cursor.lastrowid

# Generate random weather conditions
def generate_weather(level):
    conditions = ["Sunny", "Windy", "Rainy", "Snowy"]
    return {
        'condition': conditions[level-1],
        'temperature': random.randint(-10, 30),
        'wind_speed': random.randint(5, 40),
        'humidity': random.randint(50, 100),
        'visibility': random.randint(5, 20)
    }

# Insert weather data
def create_weather(cursor, weather):
    cursor.execute("""
        INSERT INTO Weather (`weather_condition`, temperature, wind_speed, humidity, visibility)
        VALUES (%s, %s, %s, %s, %s)
    """, (weather['condition'], weather['temperature'], weather['wind_speed'], weather['humidity'], weather['visibility']))
    return cursor.lastrowid

# Calculate distance in kms using Haversine Formula
def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in km
    R = 6371.0
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Distance in km

    return distance

# Calculate Flight Duration using Haversine Formula
def calculate_flight_duration(departure_airport, arrival_airport):
    # Assuming the returned tuple structure is (id, name, latitude_deg, longitude_deg)
    dep_lat, dep_lon = departure_airport[2], departure_airport[3]  # Indices for latitude and longitude
    arr_lat, arr_lon = arrival_airport[2], arrival_airport[3]  # Same for arrival airport

    # Calculate distance using the Haversine formula
    distance = calculate_distance(dep_lat, dep_lon, arr_lat, arr_lon)

    # Assuming a static speed in km/h, the speed of airplane is set as 800 to calculate the duration
    # from departure airport to the arrival airport
    speed = 800
    duration_hours = distance / speed

    # Return a timedelta and distance
    flight_duration = timedelta(hours=duration_hours)
    return flight_duration, distance

# Reimporting Datetime
import datetime
# Game loop
def start_flight(departure_airport, arrival_airport, flight_duration, weather, cursor, user_id, level):
    print("\nGame Started!")
    print(f"Flying from {departure_airport[1]} to {arrival_airport[1]}.")
    print(f"Weather: {weather['condition']}, Temp: {weather['temperature']}°C, Wind Speed: {weather['wind_speed']} km/h")
    print("Please fasten your seatbelt. The flight has some unexpected challenges.")

    # Flight start time
    start_time = datetime.datetime.now()

    # Present level-based hurdles to the player
    hurdles = get_hurdles_for_level(level)
    time.sleep(3)

    for hurdle in hurdles:
        print("\n--- Challenge ---")
        print(hurdle['description'])
        user_choice = input("Choose an option (1 or 2): ")

        if int(user_choice) == hurdle['correct_option']:
            print(f"Success: {hurdle['result']}")
        else:
            print("Wrong choice! You are blown away! Game Over.")
            return False, datetime.datetime.now() - start_time

    # If successful, calculate total flight time
    end_time = datetime.datetime.now()
    total_flight_time = end_time - start_time
    print("\nCongratulations! You have completed the flight successfully.")
    print(f"Total flight duration: {total_flight_time}")

    return True, total_flight_time

def play_game():
    start_game = input("Do you want to play the game? (yes/no): ").lower()

    # If the user chooses 'no', terminate the game
    if start_game != "yes":
        print("Exiting the game. Have a nice day!")
        return

    connection = connect_database()
    cursor = connection.cursor(buffered=True)

    # User creation or fetching using get_or_create_user
    username = input("\n <<<<<<<<<...Welcome to the flight simulator...>>>>>>>> \
       \n... where YOU: A Pilot, is about to take one of our Airplane to journey you have never been before.\
       \nNow follow the instructions and take a seat and find out what our game holds in for you...\
       \n\nEnter your username: ")

    user_id, fuel_consumed = get_or_create_user(cursor, username)
    if fuel_consumed is None:
        fuel_consumed = 500  # Default fuel for new users
    print(f"Your current fuel is {fuel_consumed}.")

    connection.commit()

    # Select continent and country (default Finland)
    print("\nSelect a continent: \nExample-> \n Europe: EU or eu\n Asia: AS or as\n South America: SA or sa")
    continent = input("Continent: ")
    print("\nCountry. Write ISO of country: \nExample-> \n FI or fi for Finland.\n AE or ae for Abu Dhabi\n AR or ar for Arizona")
    country = input("Country: ") or "FI"

    # Display airports based on both country and continent
    airports = get_airports_for_country_and_continent(cursor, country, continent)
    if not airports:
        print(f"No airports available for {country} in {continent}.")
        return

    print("\nAvailable airports:")
    for idx, airport in enumerate(airports):
        print(f"{idx + 1}. {airport[1]} ({airport[2]})")

    # Select the Departure airport
    while True:
        try:
            departure_index = int(input("Select Departure Airport (Write the index number corresponding to the airport name in above list): ")) - 1
            departure_airport = airports[departure_index]
            break # exit the loop if selection is valid
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid index.")

    while True:
        try:
            arrival_index = int(input("Select Arrival Airport (Write the index number corresponding to the airport name in above list): ")) - 1
            arrival_airport = airports[arrival_index]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid index.")

    # Get scheduled departure time
    departure_time_str = input("Enter scheduled departure time (YYYY-MM-DD): ")
    scheduled_departure_time = datetime.datetime.strptime(departure_time_str, '%Y-%m-%d')

    # Automatically generate arrival time
    flight_duration, distance = calculate_flight_duration(departure_airport, arrival_airport)
    scheduled_arrival_time = scheduled_departure_time + flight_duration

    print(f"Flight Details:\nFrom: {departure_airport[1]} to {arrival_airport[1]}")
    print(f"Distance: {distance:.2f} km, Flight Time: {flight_duration}")

    # Start with initial weather
    weather = generate_weather(1)
    level = 1
    total_flight_time = datetime.timedelta()

    # Game loop
    while fuel_consumed > 0:
        print(f"\nLevel {level}: Weather Condition - {weather['condition']}")
        hurdles = get_hurdles_for_level(level)
        print(f"Your current fuel: {fuel_consumed}")

        for hurdle in hurdles:
            print("\n--- Challenge ---")
            print(hurdle['description'])
            user_choice = input("Choose an option (1 or 2): ")

            # print("Hurdle data:", hurdle)

            # Adjust fuel based on challenge result
            complexity_percentage = hurdle['complexity'] / 100.0
            if int(user_choice) == hurdle['correct_option']:
                print(f"Success: {hurdle['result']}")
                fuel_increase = fuel_consumed * complexity_percentage
                fuel_consumed += fuel_increase
                print(f"Fuel increased by {fuel_increase:.2f}. New fuel: {fuel_consumed:.2f}")
            else:
                print("Wrong choice! You lost the challenge.")
                fuel_loss = fuel_consumed * complexity_percentage
                fuel_consumed -= fuel_loss
                print(f"Fuel decreased by {fuel_loss:.2f}. New fuel: {fuel_consumed:.2f}")
                if fuel_consumed <= 0:
                    print("You ran out of fuel! Game Over.")
                    return

        # Progress to the next level
        total_flight_time += flight_duration
        level += 1
        if level > 4:
            print("Congratulations! You've completed the game.")
            break

        # Generate harder weather for the next level
        weather = generate_weather(level)

    # Insert flight log and update fuel
    weather_id = create_weather(cursor, weather)
    flight_id = create_flight(cursor, departure_airport[0], arrival_airport[0], scheduled_departure_time,
                              scheduled_arrival_time)
    cursor.execute("""
            INSERT INTO User_Flight_Log (user_id, flight_id, weather_id, flight_time, completion_status, created_at)
            VALUES (%s, %s, %s, NOW(), %s, NOW())
        """, (user_id, flight_id, weather_id, "Success"))
    cursor.execute("UPDATE User SET fuel_consumed = %s WHERE id = %s", (fuel_consumed, user_id))
    connection.commit()

    print(f"Total flight time: {total_flight_time}, Final fuel: {fuel_consumed:.2f}")

    # Close connection
    cursor.close()
    connection.close()

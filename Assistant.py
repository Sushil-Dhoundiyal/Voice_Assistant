
import speech_recognition as sr  # Library for recognizing speech
import pyttsx3  # Library for text-to-speech conversion
import pywhatkit  # Library to automate web-based tasks like playing YouTube videos
import datetime  # For working with date and time
import wikipedia  # For accessing Wikipedia articles
import webbrowser  # To open web pages in the default browser
import sys  # Provides access to some variables used or maintained by the interpreter
import time  # Provides time-related functions
import requests  # To send HTTP requests (used for fetching weather data)

# Initialize speech recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Global flag to control the main loop
running = True

# Function to make Alexa speak out loud
def talk(text):
    engine.say(text)  # Pass text to the engine for speech
    engine.runAndWait()  # Ensure speech is completed before moving on

# Function to capture and recognize the voice command
def take_command():
    command = ""  # Initialize an empty command
    try:
        with sr.Microphone() as source:  # Use the microphone as the input source
            print('listening...')
            listener.adjust_for_ambient_noise(source)  # Adjust to background noise levels
            voice = listener.listen(source, timeout=5, phrase_time_limit=5)  # Listen for the command with a timeout
            command = listener.recognize_google(voice)  # Use Google API to recognize speech
            command = command.lower()  # Convert the command to lowercase
            if 'alexa' in command:
                command = command.replace('alexa', '')  # Remove the wake word 'alexa' from the command
                print(command)
    except sr.UnknownValueError:  # Catch unrecognized speech
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:  # Catch issues with the recognition service
        print(f"Could not request results; {e}")
    except Exception as e:  # General error catch
        print(f"Error: {e}")
        pass
    return command  # Return the recognized command

# Function to fetch weather information for a given city
def get_weather(city):
    API_KEY = 'your_openweathermap_api_key'  # Your OpenWeatherMap API key
    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'  # API endpoint
    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"  # Build request URL with city and API key
    response = requests.get(url)  # Send the GET request to the API
    data = response.json()  # Parse the JSON response
    if data['cod'] == 200:  # Check if the request was successful
        main = data['main']  # Extract main weather data
        weather = data['weather'][0]['description']  # Extract weather description
        temp = main['temp']  # Extract temperature
        return f"The weather in {city} is {weather} with a temperature of {temp}°C."
    else:
        return "I couldn't fetch the weather information."  # Error message if city is not found

# Main function to run Alexa and process commands
def run_alexa():
    global running
    command = take_command()  # Capture the voice command
    print(f"Processing command: {command}")
    
    if 'play' in command:  # If command asks to play a song
        song = command.replace('play', '').strip()  # Extract song name
        if song:
            talk('Playing ' + song)
            pywhatkit.playonyt(song)  # Use pywhatkit to play the song on YouTube
        else:
            talk("I didn't catch the name of the song.")

    elif 'time' in command:  # If command asks for the current time
        time = datetime.datetime.now().strftime('%I:%M %p')  # Get current time in 12-hour format
        talk('Current time is ' + time)

    elif 'open wikipedia' in command:  # If command asks to open a Wikipedia page
        topic = command.replace('open wikipedia', '').strip()  # Extract topic
        if topic:
            url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"  # Build Wikipedia URL
            talk(f'Opening Wikipedia page for {topic}')
            webbrowser.open(url)  # Open the Wikipedia page in the default browser
        else:
            talk("I didn't catch the topic.")

    elif 'tell me weather' in command:  # If command asks for the weather
        city = command.replace('weather in', '').strip()  # Extract city name
        if city:
            weather_info = get_weather(city)  # Fetch weather data
            talk(weather_info)
            print(weather_info)
        else:
            talk("I didn't catch the city name.")

    elif 'set reminder' in command:  # If command asks to set a reminder
        try:
            parts = command.split('in')  # Split command into reminder text and time
            if len(parts) == 2:
                reminder_text = parts[0].replace('set reminder', '').strip()  # Extract reminder text
                delay_part = parts[1].strip().split()  # Extract the delay part (e.g., '5 minutes')
                if len(delay_part) > 0:
                    delay_minutes = int(delay_part[0])  # Convert the first part to an integer (minutes)
                    set_reminder(reminder_text, delay_minutes)  # Call the set reminder function
                else:
                    talk("I didn't catch the number of minutes.")
            else:
                talk("I didn't catch the reminder details.")
        except ValueError:
            talk("I didn't understand the number of minutes for the reminder.")

    elif 'stop' in command or 'exit' in command:  # If command is to stop Alexa
        talk('Stopping Alexa')
        running = False  # Set flag to stop the loop

    elif 'date' in command:  # Funny response to 'date' command
        talk('Your, Time is good')

    elif 'are you single' in command:  # Response to 'are you single' command
        talk('I am in a relationship with Python and its libraries')

    else:  # If command doesn't match any of the above
        talk('Please say the command again.')

# Keep running Alexa in a loop until the user says 'stop' or 'exit'
while running:
    run_alexa()

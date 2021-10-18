from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
import requests
import random
import json

from .weather import get_weather, generate_weather_message
from django.conf import settings

@csrf_exempt
def index(request):

    if request.method == 'POST':

        incoming_message = request.POST.get('Body').lower()
        valid_response = False

        if "hello" in incoming_message:
            hello_response = generate_message("hello")
            valid_response = True
            final_response = send_message(hello_response)

        if "weather" in incoming_message:
            location_response = generate_message("weather")
            valid_response = True
            final_response = send_message(location_response)   

        try:
            lat = request.POST.get('Latitude')
            lon = request.POST.get('Longitude')
            if lat and lon:
                valid_response = True
                weather_response = generate_weather_message(get_weather(lat, lon, settings.OPEN_WEATHER_API_KEY))
            final_response = send_message(weather_response)
                
        except:
            print('no location data found')

        if "cat" in incoming_message:
            valid_response = True
            media = 'https://cataas.com/cat'
            final_response = send_message("Here is a cat!", media)
        
        # if "directions" in incoming_message:
        #     response = generate_message("directions")
        #     valid_response = True
        #     final_response = send_message(response)
        
        # if "music" in incoming_message:
        #     response = generate_message("music")
        #     valid_response = True
        #     final_response = send_message(response)

        # if "melody" in incoming_message:
        #     response = generate_message("melody")
        #     valid_response = True
        #     final_response = send_message(response)

        if "funny" in incoming_message:
            valid_response = True

            subreddit = "memes"
            listing = "hot"
            limit = 100
            timeframe = "month"
            funny_response = get_reddit(subreddit, listing, limit, timeframe)

            if funny_response.status_code == 200:
                json_file = funny_response.json()
                reddit_posts = json_file['data']['children']
                random_post = random.choice(reddit_posts)
                post_data = random_post['data']
                title = post_data['title']
                media = post_data['url']

                if media.endswith(".gif"):
                    title += "\nThis media response contains a .gif file. The Twilio API for WhatsApp does not support the .gif filetype at this time."

            final_response = send_message(title, media)

        if "wholesome" in incoming_message:
            valid_response = True

            subreddit = "wholesomememes"
            listing = "hot"
            limit = 100
            timeframe = "month"
            wholesome_response = get_reddit(subreddit, listing, limit, timeframe)

            if wholesome_response.status_code == 200:
                json_file = wholesome_response.json()
                reddit_posts = json_file['data']['children']
                random_post = random.choice(reddit_posts)
                post_data = random_post['data']
                title = post_data['title']
                media = post_data['url']
                
                if media.endswith(".gif"):
                    title += "\nThis media response contains a .gif file. The Twilio API for WhatsApp does not support the .gif filetype at this time."

            final_response = send_message(title, media)

        # if "game" in incoming_message:
        #     game_response = generate_message("game")
        #     valid_response = True
        #     final_response = send_message(game_response)

        # if "stocks" in incoming_message:
        #     stocks_response = generate_message("stocks")
        #     valid_response = True
        #     final_response = send_message(stocks_response)
        
        if not valid_response:
            response = generate_message("invalid")
            valid_response = True
            final_response = send_message(response)

        return HttpResponse(str(final_response))
        

        # \nEnter *directions* to get directions to a location.\
        # \nEnter *music* to play a track on Spotify.\
        # \nEnter *melody* to listen to variations of your favorite song.\
        # \nEnter *game* to play a game.
        # \nEnter *stocks* to view stocks.
        

def generate_message(message):
    if message == "hello":
        return "Greetings! \
        \nEnter *weather* to check the weather.\
        \nEnter *cat* to see a picture of a cat. \
        \nEnter *funny* to see a funny meme.\
        \nEnter *wholesome* to see a wholesome meme."

    elif message == "weather":
        return "Send me your location."
    # elif message == "directions":
    #     return "you chose directions"
    # elif message == "music":
    #     return "you chose music"
    # elif message == "melody":
    #     return "you chose melody"
    # elif message == "game":
    #     return "you chose game"
    # elif message == "stocks":
    #     return "you chose stocks"
    elif message == "invalid":
        return "Enter *hello* to get started and see available options."

def get_reddit(subreddit, listing, limit, timeframe):
    url = f"https://www.reddit.com/r/{subreddit}/{listing}.json?limit={limit}?t={timeframe}"
    response = requests.get(url, headers = {'User-agent': 'sventwiliobot'})
    return response

def send_message(message, media_url = None):
    response = MessagingResponse()
    response.message().body(message)
    response.message().media(media_url)
    return response

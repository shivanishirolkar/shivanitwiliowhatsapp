# shivanitwiliowhatsapp
This is a project I am using to play around with the Twilio API for WhatsApp. I created a simple chatbot in Python using the Django web framework. It is equipped to receive and handle WhatsApp messages depending on the keywords they contain.

## Prerequisites
1. Python 3.6 or newer
2. A Twilio account
3. A smartphone with an active WhatsApp account

## How to deploy:
1. Create a free Twilio account and set up the Sandbox for Whatsapp [here](https://www.twilio.com/console/sms/whatsapp/sandbox).
2. Open a terminal and clone this repository. Use ```$ pip install -r requirements.txt``` to install the dependencies.
3. Navigate to the root directory and run the following commands to start the application: <br />
   ```$ python manage.py migrate```<br />
   ```$ python manage.py runserver```
5. Open another terminal and type in the command ```ngrok http 8000```. It will output a summary of the session status. Copy the URL next to Forwarding; it should look like this: ```https://d9ee-203-13-181-11.ngrok.io```.
6. Append ```/message``` to the end of this URL and paste it into the webhook for "WHEN A MESSAGE COMES IN" under Sandbox Configuration. Set the request to HTTP POST.
7. Click save and send "hello" to the Twilio bot on WhatsApp.

## Things in progress:
1. Weather functionality
2. Deployment on a hosting service

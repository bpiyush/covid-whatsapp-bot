
### Instructions for new users

1. Connect to the Twilio-sandbox bot by sending a WhatsApp message to the number +1 415 523 8886
```bash
join unknown-back
```

2. Send an introductory message
```bash
hello
```
<!-- 
3. Enter your city name
```bash
City: Mumbai
```

4. Enter your resource requirement
```bash
Req: Oxygen
```

5. You shall find resources in the following format.


6. Post this, if you have any feedback, please drop a message:
```bash
Feedback: xyz
``` -->
3. Enter your city/town and requirements in the following format:
```bash
Help
City: Mumbai
Req: Oxygen
```
You shall find resources in the following format.


### Instructions for developers

1. Clone the repo; go to the repo
```bash
git clone XXXX
cd covid-whatsapp-bot/
```

2. Set pythonpath
```bash
export PYTHONPATH=$PWD
```

3. Run the server locally
```bash
cd bot/
python manage.py runserver
```
You should expect an output like this:
```bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
April 25, 2021 - 12:36:51
Django version 3.2, using settings 'bot.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

4. Fire `ngrok` server on port 8000
```bash
ngrok http 8000
```
You should expect an output like this:
```bash
ngrok by @inconshreveable                                                                                                                                                (Ctrl+C to quit)

Session Status                online
Session Expires               1 hour, 59 minutes
Version                       2.3.39
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://xxxxxxxxxx.ngrok.io -> http://localhost:8000
Forwarding                    https://xxxxxxxxxx.ngrok.io -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```
The `xxxxxxxx` will denote your server address. You need to enter `http://xxxxxxxxxx.ngrok.io/bot/` into the Twilio Sandbox to enable messaging via this server.
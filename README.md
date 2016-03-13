[![Build Status](https://travis-ci.org/azam-a/gocd2gmail2slack.svg?branch=master)](https://travis-ci.org/azam-a/gocd2gmail2slack) [![Coverage Status](https://coveralls.io/repos/azam-a/gocd2gmail2slack/badge.svg?branch=master&service=github)](https://coveralls.io/github/azam-a/gocd2gmail2slack?branch=master)

of course there are more elegant solutions like [gmail2slack](https://github.com/brooksc/gmail2slack) 
or [gocd-slack-build-notifier](https://github.com/ashwanthkumar/gocd-slack-build-notifier), 
but in cases of permission constraints to the gocd environment and the only available channel is email, 
then maybe this solution is acceptable. nevertheless, it was a good learning exercise for me.


## How to use

1. Turn on Gmail API for a Google Account ([instructions Step 1](https://developers.google.com/gmail/api/quickstart/python)) and get the ```client_secret.json``` to register the app
2. Clone this repo
3. In activated virtualenv session (or global environment), install required packages from `requirements.txt`:

    ```
    pip install -r requirements.txt
    ```
4. Edit ```config.py``` to include Slack Incoming Webhook and GoCD dashboard URLs ([template](https://github.com/azam-a/gocd2gmail2slack/blob/master/gocd2gmail2slack/cfg/config.py))
5. Paste the ```client_secret.json``` from Step 1 into the ```cfg``` [folder](https://github.com/azam-a/gocd2gmail2slack/blob/master/gocd2gmail2slack/cfg/)
6. ```cd``` into the ```gocd2gmail2slack``` directory (which contains ```integrations.py```)
7. (optional) To run tests, run ```python -m unittest``` from the same directory as Step 6
6. Create a Gmail label ```'SENT_TO_SLACK'``` at the intended Gmail account
8. run ```python integrations.py```
9. The first run will open a browser to authenticate and authorize a Gmail account
10. The credentials will be saved to ```cfg/cred/saved_credentials.json``` for subsequent runs
11. The script will query all the ```'UNREAD'``` emails and process them accordingly
12. Schedule the running of ```python integrations.py``` every X minutes using Task Scheduler or Cron

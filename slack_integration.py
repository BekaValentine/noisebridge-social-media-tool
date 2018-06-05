import requests
from flask import Flask, request
import TwitterAction
import secrets # includes SLACK_WEBHOOK_URL plus some SLACK_TOKENS



def log_to_slack(action):
    payload = {
        "channel": "#hook-testing",
        "username": "social-media-tool",
        "text": action.slack_message(),
        "icon_emoji": action.icon_emoji
    }
    print("Logging action: ", action)
    print(action.slack_message())
    #return requests.post(SLACK_WEBHOOK_URL, json=payload)






app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello SMT!"



@app.route("/slack/twitter/make", methods=['POST'])
def twitter_make():
    
    #if request.form['token'] != APPROVE_SLACK_TOKEN:
    #    return ':('
    
    #slack_handle = request.form['user_name']
    #content = request.form['text']
    #attachments = []
    
    print("foo")
    #log_to_slack(TwitterAction.Make(slack_handle, content, attachments))



#@app.route("/slack/twitter/make-attachments", methods=['POST'])
def twitter_make_attachments():

    if request.form['token'] != APPROVE_SLACK_TOKEN:
        return ':('

    slack_handle = request.form['user_name']
    parts = request.form['text'].split(',', maxsplit=1)
    content = parts[1]
    attachments = parts[0].split(',')

    log_to_slack(TwitterAction.Make(slack_handle, content, attachments))



if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3115)
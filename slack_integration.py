import requests
from flask import Flask, request
import TwitterAction
from secrets import * # includes SLACK_WEBHOOK_URL plus some SLACK_TOKENS



def log_to_slack(action):
    payload = {
        "channel": "#hook-testing",
        "username": "social-media-tool",
        "text": action.slack_message(),
        "icon_emoji": action.icon_emoji
    }
    print("Logging action: ", action)
    print(action.slack_message())
    return requests.post(SLACK_WEBHOOK_URL, json=payload)






app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello SMT!"



@app.route("/slack/twitter/make", methods=['POST'])
def twitter_make():
    
    if request.form['token'] != SLACK_TWITTER_MAKE_TOKEN:
        return ':('
    
    user_id = request.form['user_id']
    content = request.form['text']
    attachments = []
    
    log_to_slack(TwitterAction.Make(user_id, content, attachments))
    return ""



@app.route("/slack/twitter/make-attachments", methods=['POST'])
def twitter_make_attachments():

    if request.form['token'] != SLACK_TWITTER_MAKE_ATTACHMENTS_TOKEN:
        return ':('

    user_id = request.form['user_id']
    parts = request.form['text'].split(';',1)
    content = parts[1]
    attachments = parts[0].split(',')
    
    log_to_slack(TwitterAction.Make(user_id, content, attachments))
    return ""



if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3115)
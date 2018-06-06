import requests
from flask import Flask, request
import SocialMediaAction
import TwitterService
from secrets import * # includes SLACK_WEBHOOK_URL plus some SLACK_TOKENS



def log_to_slack(action):
    payload = {
        "channel": "#hook-testing",
        "username": "social-media-tool",
        "text": action.slack_message(),
        "icon_emoji": action.icon_emoji
    }
    print("Logging action: ", action.slack_message())
    return requests.post(SLACK_WEBHOOK_URL, json=payload)


def unknown_service_error(service):
    payload = {
        "channel": "#hook-testing",
        "username": "social-media-tool",
        "text": "I'm sorry, I don't know about the social media service named " + service,
        "icon_emoji": ":vibration_mode:"
    }
    return requests.post(SLACK_WEBHOOK_URL, json=payload)






app = Flask(__name__)



@app.route("/")
def hello():
    return "Hello SMT!"


###
### Services record
###

SERVICES = { \
  "twitter": TwitterService.TwitterService() \
}




###
### Utilities
###

def split_service(text):
  service, rest = text.split(":",1)
  return (service.strip(), rest.strip())

def split_attachments(text):
  attachments, rest = text.split(";",1)
  return (map(lambda a: a.strip(), attachments.split(",")), rest.strip())






###
### Routing
###



@app.route("/slack/make", methods=['POST'])
def twitter_make():
    
    if request.form['token'] != SLACK_MAKE_TOKEN:
        return ':('
    
    service, content = split_service(request.form['text'])
    
    if (service not in SERVICES):
      unknown_service_error(service)
      return ":("
    
    user_id = request.form['user_id']
    attachments = []
    
    action = SocialMediaAction.Make(SERVICES[service], user_id, content, attachments)
    action.handle()
    
    log_to_slack(action)
    
    return ""



@app.route("/slack/make-attachments", methods=['POST'])
def twitter_make_attachments():

    if request.form['token'] != SLACK_MAKE_ATTACHMENTS_TOKEN:
        return ':('
    
    service, rest = split_service(request.form['text'])
    
    if (service not in SERVICES):
      unknown_service_error(service)
      return ":("
      
    user_id = request.form['user_id']
    
    attachments, content = split_attachments(rest)
    
    action = SocialMediaAction.Make(Twitter, user_id, content, attachments)
    
    log_to_slack(action)
    
    return ""



@app.route("/slack/twitter/reply", methods=['POST'])
def twitter_reply():

    if request.form['token'] != SLACK_TWITTER_REPLY_TOKEN:
        return ':('

    user_id = request.form['user_id']
    parts = request.form['text'].split(";",1)
    reply_to_url = parts[0].strip()
    content = parts[1].strip()
    attachments = []
    
    action = SocialMediaAction.Reply(Twitter, user_id, reply_to_url, content, attachments)
    
    log_to_slack(action)
    return ""



@app.route("/slack/twitter/reply-attachments", methods=['POST'])
def twitter_reply_attachments():

    if request.form['token'] != SLACK_TWITTER_REPLY_ATTACHMENTS_TOKEN:
        return ':('

    user_id = request.form['user_id']
    parts = request.form['text'].split(';',2)
    reply_to_url = parts[0].strip()
    content = parts[2].strip()
    attachments = parts[1].strip().split(',')
    
    action = SocialMediaAction.Reply(Twitter, user_id, reply_to_url, content, attachments)
    
    log_to_slack(action)
    return ""



@app.route("/slack/twitter/delete", methods=['POST'])
def twitter_delete():

    if request.form['token'] != SLACK_TWITTER_DELETE_TOKEN:
        return ':('

    user_id = request.form['user_id']
    deleted_tweet_url = request.form['text']
    deleted_tweet_content = ""

    action = SocialMediaAction.Delete(Twitter, user_id, deleted_tweet_url, deleted_tweet_content)

    log_to_slack(action)
    return ""



@app.route("/slack/twitter/share", methods=['POST'])
def twitter_share():

    if request.form['token'] != SLACK_TWITTER_SHARE_TOKEN:
        return ':('

    user_id = request.form['user_id']
    shared_tweet_url = request.form['text']

    action = SocialMediaAction.Share(Twitter, user_id, shared_tweet_url)

    log_to_slack(action)
    return ""



@app.route("/slack/twitter/unshare", methods=['POST'])
def twitter_unshare():

    if request.form['token'] != SLACK_TWITTER_UNSHARE_TOKEN:
        return ':('

    user_id = request.form['user_id']
    unshared_tweet_url = request.form['text']

    action = SocialMediaAction.Unshare(Twitter, user_id, unshared_tweet_url)

    log_to_slack(action)
    return ""



if __name__ == '__main__':
  app.run(host='127.0.0.1', port=3115)
import requests
from flask import Flask, request
import SocialMediaAction
import TwitterService
import threading
from config import *
from secrets import * # includes SLACK_WEBHOOK_URL plus some SLACK_TOKENS

def log_action_to_slack(action):
    payload = {
        "channel": SMT_CHANNEL,
        "username": SMT_USERNAME,
        "text": action.slack_message(),
        "icon_emoji": action.icon_emoji
    }
    return requests.post(SLACK_WEBHOOK_URL, json=payload)

def elongate_request(work, msg=""):
  half_hour_url = request.form['response_url']
  def task():
    ret = work()
    if ret:
      res = requests.post(half_hour_url, json={"text": ret})
  t = threading.Thread(target=task)
  t.start()
  return msg

app = Flask(__name__)
application = app # <- for wsgi

@app.route("/")
def hello():
    return "Hello SMT!"


"""
Services record
"""
SERVICES = { \
  "twitter": TwitterService.TwitterService(TWITTER_KEYS) \
}


"""
Utilities
"""
def malformed_input_error_message(format):
  return ":warning: The input you gave is malformed. It should have the format `" + format + "`."


def unknown_social_media_service_error_message(service_name):
  return ":warning: There is no social media service named `" + service_name + "`. The known services are: `" + "`, `".join(SERVICES.keys()) + "`."


def split_service_name(text):
  if -1 != text.find(":"):
    service_name, rest = text.split(":",1)
    return (False, service_name.strip(), rest.strip())
  else:
    return (True, None, None)


def lookup_service(service_name):
  service_name = service_name.lower()
  if service_name in SERVICES:
    return (False, SERVICES[service_name])
  else:
    return (True, None)


def split_attachments(text):
  if -1 != text.find(";"):
    attachments, rest = text.split(";",1)
    return (False, list(map(lambda a: a.strip(), attachments.split(","))), rest.strip())
  else:
    return (True, None, None)


def split_url(text):
  if -1 != text.find(";"):
    url, rest = text.split(";",1)
    return (False, url.strip(), rest.strip())
  else:
    return (True, None, None)


"""
Routing
"""

MAKE_FORMAT = "[service]: [content]"

@app.route("/slack/make", methods=['POST'])
def make():
    if request.form['token'] != SLACK_MAKE_TOKEN:
        return ':('
    user_id = request.form['user_id']

    err, service_name, content = split_service_name(request.form['text'])
    if err: return malformed_input_error_message(MAKE_FORMAT)

    err, service = lookup_service(service_name)
    if err: return unknown_social_media_service_error_message(service_name)
    attachments = []
    action = SocialMediaAction.Make(service, user_id, content, attachments)
    def the_rest():
        action.handle()
        log_action_to_slack(action)
        return ""
    return elongate_request(the_rest, "Posting to " + service_name + " ...")



MAKE_ATTACHMENTS_FORMAT = "[service]: [attachment], ...; [content]"

@app.route("/slack/make-attachments", methods=['POST'])
def make_attachments():
    if request.form['token'] != SLACK_MAKE_ATTACHMENTS_TOKEN:
        return ':('

    user_id = request.form['user_id']

    err, service_name, rest = split_service_name(request.form['text'])
    if err: return malformed_input_error_message(MAKE_ATTACHMENTS_FORMAT)

    err, service = lookup_service(service_name)
    if err: return unknown_social_media_service_error_message(service_name)

    err, attachments, content = split_attachments(rest)
    if err: return malformed_input_error_message(MAKE_ATTACHMENTS_FORMAT)

    action = SocialMediaAction.Make(service, user_id, content, attachments)

    def the_rest():
        err, message = action.handle()
        if err: return message
        log_action_to_slack(action)

    return elongate_request(the_rest, "Posting to " + service_name + " ...")


REPLY_FORMAT = "[service]: [url]; [content]"

@app.route("/slack/reply", methods=['POST'])
def reply():
    if request.form['token'] != SLACK_REPLY_TOKEN:
        return ':('

    user_id = request.form['user_id']

    err, service_name, rest = split_service_name(request.form['text'])
    if err: return malformed_input_error_message(REPLY_FORMAT)

    err, service = lookup_service(service_name)
    if err: return unknown_social_media_service_error_message(service_name)

    err, reply_to_url, content = split_url(rest)
    if err: return malformed_input_error_message(REPLY_FORMAT)

    attachments = []

    action = SocialMediaAction.Reply(service, user_id, reply_to_url, content, attachments)

    def the_rest():
        err, message = action.handle()
        if err: return message
        log_action_to_slack(action)

    return elongate_request(the_rest, "Posting to " + service_name + " ...")

REPLY_ATTACHMENTS_FORMAT = "[service]: [url]; [attachment], ... ; [content]"

@app.route("/slack/reply-attachments", methods=['POST'])
def reply_attachments():
    if request.form['token'] != SLACK_REPLY_ATTACHMENTS_TOKEN:
        return ':('

    user_id = request.form['user_id']

    err, service_name, rest = split_service_name(request.form['text'])
    if err: return malformed_input_error_message(REPLY_ATTACHMENTS_FORMAT)

    err, service = lookup_service(service_name)
    if err: return unknown_social_media_service_error_message(service_name)

    err, reply_to_url, rest = split_url(rest)
    if err: return malformed_input_error_message(REPLY_ATTACHMENTS_FORMAT)

    err, attachments, content = split_attachments(rest)
    if err: return malformed_input_error_message(REPLY_ATTACHMENTS_FORMAT)

    action = SocialMediaAction.Reply(service, user_id, reply_to_url, content, attachments)

    def the_rest():
        err, message = action.handle()
        if err: return message
        log_action_to_slack(action)

    return elongate_request(the_rest, "Posting to " + service_name + " ...")


DELETE_FORMAT = "[service]: [url]"

@app.route("/slack/delete", methods=['POST'])
def delete():
    if request.form['token'] != SLACK_DELETE_TOKEN:
        return ':('

    user_id = request.form['user_id']

    err, service_name, deleted_post_url = split_service_name(request.form['text'])
    if err: return malformed_input_error_message(DELETE_FORMAT)

    err, service = lookup_service(service_name)
    if err: return unknown_social_media_service_error_message(service_name)

    deleted_post_content = ""

    action = SocialMediaAction.Delete(service, user_id, deleted_post_url, deleted_post_content)

    def the_rest():
        err, message = action.handle()
        if err: return message
        log_action_to_slack(action)

    return elongate_request(the_rest, "Deleting from " + service_name + " ...")

SHARE_FORMAT = "[service]: [url]"

@app.route("/slack/share", methods=['POST'])
def share():
    if request.form['token'] != SLACK_SHARE_TOKEN:
        return ':('

    user_id = request.form['user_id']
    err, service_name, shared_post_url = split_service_name(request.form['text'])
    if err: return malformed_input_error_message(SHARE_FORMAT)

    err, service = lookup_service(service_name)
    if err: return unknown_social_media_service_error_message(service_name)

    action = SocialMediaAction.Share(service, user_id, shared_post_url)

    def the_rest():
        err, message = action.handle()
        if err: return message
        log_action_to_slack(action)

    return elongate_request(the_rest, "Posting to " + service_name + " ...")


UNSHARE_FORMAT = "[service]: [url]"

@app.route("/slack/unshare", methods=['POST'])
def unshare():
    if request.form['token'] != SLACK_UNSHARE_TOKEN:
        return ':('

    user_id = request.form['user_id']

    err, service_name, unshared_post_url = split_service_name(request.form['text'])
    if err: return malformed_input_error_message(UNSHARE_FORMAT)

    err, service = lookup_service(service_name)
    if err: return unknown_social_media_service_error_message(service_name)

    action = SocialMediaAction.Unshare(service, user_id, unshared_post_url)

    def the_rest():
        err, message = action.handle()
        if err: return message
        log_action_to_slack(action)

    return elongate_request(the_rest, "Removing from " + service_name + " ...")


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3116)

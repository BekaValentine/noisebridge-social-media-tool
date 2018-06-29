from SocialMediaService import SocialMediaService
import twitter # install with `pip install python-twitter`
from twitter.error import TwitterError

def status_url(status):
    return "https://twitter.com/" + status.user.screen_name + "/status/" + status.id_str

def retweet_url(status):
    return "https://twitter.com/" + status.retweeted_status.user.screen_name + "/status/" + status.retweeted_status.id_str

def bad_attachments(attachments):
    #return not all(map(lambda url: url.startswith("http") or url.startswith("https")))
    for url in attachments:
      if not url.startswith("http://") and not url.startswith("https://"):
        return True
    
    return False

class TwitterService(SocialMediaService):
    def __init__(self, keys):
        self.name = "Twitter"
        self.verb_made = "tweeted"
        self.verb_shared = "retweeted"
        self.noun_post = "tweet"
        self.keys = keys
        self.api = twitter.Api(consumer_key=self.keys['consumer'],
                               consumer_secret=self.keys['consumer_secret'],
                               access_token_key=self.keys['access'],
                               access_token_secret=self.keys['access_secret']
                               )

    # Returns: new post URL
    def make(self, content, attachments):
        
        if bad_attachments(attachments):
          return True, "Attachments must be http(s) URLs."
        
        try:
          status = self.api.PostUpdate(content, media=attachments)
          return False, status_url(status)
        except TwitterError as e:
          return True, "An error has occurred:" + e.message[0]["message"]

    # Returns: new reply URL
    def reply(self, post_url, content, attachments):
        
        if bad_attachments(attachments):
          return True, "Attachments must be http(s) URLs."
        
        try:
          post_id = post_url.split("/")[-1]
          status = self.api.PostUpdate(content,
                                       in_reply_to_status_id=post_id,
                                       exclude_reply_user_ids=None,
                                       media=attachments)
          return False, status_url(status)
        except TwitterError as e:
          return True, "An error has occurred: " + e.message[0]["message"]

    # Returns: deleted post content
    def delete(self, post_url):
        post_id = post_url.split("/")[-1]
        try:
          status = self.api.DestroyStatus(post_id)
          return False, status.text
        except TwitterError as e:
          return True, "An error has occurred: " + e.message[0]["message"]

    def share(self, post_url):
        post_id = post_url.split("/")[-1]
        try:
          status = self.api.PostRetweet(post_id)
          return False, status_url(status)
        except TwitterError as e:
          return True, "An error has occurred: " + e.message[0]["message"]

    def unshare(self, post_url):
        post_id = post_url.split("/")[-1]
        try:
          status = self.api.DestroyStatus(post_id)
          return False, retweet_url(status)
        except TwitterError as e:
          return True, "An error has occurred: " + e.message[0]["message"]

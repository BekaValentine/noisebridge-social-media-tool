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

    def extract_error_message(self, e):
        if isinstance(e.message, str):
            return e.message
        if isinstance(e.message[0], str):
            return e.message[0]
        return e.message[0]["message"]
    def catch_twitter(self, f):
        try:
            return False, f()
        except TwitterError as e:
            return True, "An error has occured: " + self.extract_error_message(e)

    # Returns: new post URL
    def make(self, content, attachments):
        if bad_attachments(attachments):
            return True, "Attachments must be http(s) URLs."
        return self.catch_twitter(lambda: status_url(self.api.PostUpdate(content, media=attachments)))

    # Returns: new reply URL
    def reply(self, post_url, content, attachments):
        if bad_attachments(attachments):
            return True, "Attachments must be http(s) URLs."
        parts = post_url.split("/")
        post_id = parts[-1]
        user_id = parts[-3]
        return self.catch_twitter(lambda: status_url(self.api.PostUpdate("@" + user_id + " " + content,
                                          in_reply_to_status_id=post_id,
                                          media=attachments)))

    # Returns: deleted post content
    def delete(self, post_url):
        post_id = post_url.split("/")[-1]
        return self.catch_twitter(lambda: self.api.DestroyStatus(post_id).text)

    def share(self, post_url):
        post_id = post_url.split("/")[-1]
        return self.catch_twitter(lambda: status_url(self.api.PostRetweet(post_id)))

    def unshare(self, post_url):
        post_id = post_url.split("/")[-1]
        return self.catch_twitter(lambda: retweet_url(self.api.DestroyStatus(post_id)))

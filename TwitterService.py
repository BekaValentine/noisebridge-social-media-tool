from SocialMediaService import SocialMediaService
import twitter # install with `pip install python-twitter`

def status_url(status):
    return "https://twitter.com/" + status.user.screen_name + "/status/" + status.id_str

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
    def make(self, content, attachments=[]):
        if attachments:
            raise ValueError("attachments are not currently supported")
        status = self.api.PostUpdate(content)
        return status_url(status)

    # Returns: new reply URL
    def reply(self, post_url, content, attachments=[], exclude_reply_user_ids=None):
        if attachments:
            raise ValueError("attachments are not currently supported")
        post_id = post_url.split("/")[-1]
        status = self.api.PostUpdate(content,
                                     in_reply_to_status_id=post_id,
                                     exclude_reply_user_ids=exclude_reply_user_ids)  # NOQA
        return status_url(status)

    # Returns: deleted post content
    def delete(self, post_url):
        post_id = post_url.split("/")[-1]
        status = self.api.DestroyStatus(post_id)
        return status.text

    def share(self, post_url, content, attachments):
        post_id = post_url.split("/")[-1]
        status = self.api.PostRetweet(post_id)
        return status_url(status)

    def unshare(self, post_url):
        return self.delete(post_url)

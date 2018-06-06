from SocialMediaService import *

class TwitterService(SocialMediaService):
  
  def __init__(self):
    self.verb_made = "tweeted"
    self.verb_shared = "retweeted"
    self.noun_post = "tweet"
  
    # Returns: new post URL
    def make(self, content, attachments):
      return "TODO"

    # Returns: new reply URL
    def reply(self, post_url, content, attachments):
      return "TODO"

    # Returns: deleted post content
    def delete(self, post_url):
      return "TODO"

    def share(self, post_url, content, attachments):
      """TODO"""

    def unshare(self, post_url):
      """TODO"""
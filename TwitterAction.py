from SocialMediaAction import *



class TwitterAction(SocialMediaAction):
  
  def __init__(self, user_id):
    SocialMediaAction.__init__(self, user_id)
    self.icon_emoji = ":twitter_icon_emoji:"
  
  def slack_message(self):
    return "A Twitter action has occurred."
  


class Make(TwitterAction):
  
  def __init__(self, user_id, content, attachments = []):
    TwitterAction.__init__(self, user_id)
    self.content = content
    self.attachments = attachments
    self.tweet_url = ""
  
  def slack_message(self):
    return "@here Human friends! " + self.user_name() + " has posted to our " +\
           "Twitter account! Be sure to share it! :)\nLink: " + self.tweet_url
  
  def handle(self):
    print("Making a new tweet.")
    self.tweet_url = "TODO"



class Reply(TwitterAction):

  def __init__(self, user_id, reply_to_url, content, attachments = []):
    TwitterAction.__init__(self, user_id)
    self.reply_to_url = reply_to_url
    self.content = content
    self.attachments = attachments
    self.reply_url = ""

  def slack_message(self):
    return "@here Human friends! " + self.user_name() + " has replied to " +\
           "a tweet via our Twitter account! Be sure to fave it! :)\nLink: " + self.reply_url

  def handle(self):
    print("Making a new reply.")
    self.reply_url = "TODO"



class Delete(TwitterAction):
  
  def __init__(self, user_id, deleted_tweet_url, deleted_tweet_content):
    TwitterAction.__init__(self, user_id)
    self.deleted_tweet_url = deleted_tweet_url
    self.deleted_tweet_content = deleted_tweet_content
  
  def slack_message(self):
    return "@here Human friends! " + self.user_name() + " has deleted a " +\
           "tweet from our Twitter account! I hope you weren't too attached " +\
           "to it!\n Deleted Tweet content: " + self.deleted_tweet_content

  def handle(self):
    print("Deleting a tweet.")



class Share(TwitterAction):
  
  def __init__(self, user_id, shared_tweet_url):
    TwitterAction.__init__(self, user_id)
    self.shared_tweet_url = shared_tweet_url
  
  def slack_message(self):
    return "@here Human friends! " + self.user_name() + " has retweeted a " +\
           "tweet from our Twitter account! Maybe you should RT it too!\n" +\
           "Retweeted Tweet: " + self.shared_tweet_url
  
  def handle(self):
    print("Sharing a tweet.")



class Unshare(TwitterAction):
  
    def __init__(self, user_id, unshared_tweet_url):
      TwitterAction.__init__(self, user_id)
      self.unshared_tweet_url = unshared_tweet_url

    def slack_message(self):
      return "@here Human friends! " + self.user_name() + " has undone a " +\
             "retweet from our Twitter account! I hope you weren't too attached " +\
             "to it!\nUnretweeted Tweet: " + self.unshared_tweet_url
    
    def handle(self):
      print("Unsharing a tweet.")
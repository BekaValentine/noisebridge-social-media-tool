class SocialMediaAction:
  
  def __init__(self, service, user_id):
    self.service = service
    self.user_id = user_id
    self.icon_emoji = ":vibration_mode:"
  
  def handle(self):
    return None
  
  def user_name(self):
    return "<@%s>" % self.user_id




class Make(SocialMediaAction):

  def __init__(self, service, user_id, content, attachments = []):
    SocialMediaAction.__init__(self, service, user_id)
    self.content = content
    self.attachments = attachments
    self.post_url = ""
  
  def handle(self):
    self.post_url = self.service.make(self.content, self.attachments)
  
  def slack_message(self):
    return "<!here> Human friends! " + self.user_name() + " has " + \
           self.service.verb_made + " on our " + self.service.name + \
           " account! Be sure to share it! :)\nLink: " + self.post_url




class Reply(SocialMediaAction):

  def __init__(self, service, user_id, reply_to_url, content, attachments = []):
    SocialMediaAction.__init__(self, service, user_id)
    self.reply_to_url = reply_to_url
    self.content = content
    self.attachments = attachments
    self.reply_url = ""
  
  def handle(self):
    self.reply_url = self.service.reply(self.reply_to_url, self.content, self.attachments)
  
  def slack_message(self):
    return "<!here> Human friends! " + self.user_name() + " has replied to " + \
           "a " + self.service.noun_post + \
           " via our " + self.service.name + " account! Be sure to fave it! :)\n" + \
           "Link: " + self.reply_url




class Delete(SocialMediaAction):

  def __init__(self, service, user_id, deleted_post_url, deleted_post_content):
    SocialMediaAction.__init__(self, service, user_id)
    self.deleted_post_url = deleted_post_url
    self.deleted_post_content = deleted_post_content
  
  def handle(self):
    self.deleted_post_content = self.service.delete(self.deleted_post_url)
  
  def slack_message(self):
    return "<!here> Human friends! " + self.user_name() + " has deleted a " + \
           self.service.noun_post + " from our " + self.service.name + \
           " account! I hope you weren't too attached to it!\n" + \
           "Deleted content: " + self.deleted_post_content




class Share(SocialMediaAction):

  def __init__(self, service, user_id, shared_post_url):
    SocialMediaAction.__init__(self, service, user_id)
    self.shared_post_url = shared_post_url
  
  def handle(self):
    self.service.share(self.shared_post_url)
  
  def slack_message(self):
    return "<!here> Human friends! " + self.user_name() + " has " + \
           self.service.verb_shared + " a " + self.service.noun_post + \
           " from our " + self.service.name + " account! Maybe you should too!\n" + \
           self.service.verb_shared + " " + self.service.noun_post + ": " + self.shared_post_url




class Unshare(SocialMediaAction):

    def __init__(self, service, user_id, unshared_post_url):
      SocialMediaAction.__init__(self, service, user_id)
      self.unshared_post_url = unshared_post_url
    
    def handle(self):
      self.service.unshare(self.unshared_post_url)
    
    def slack_message(self):
      return "<!here> Human friends! " + self.user_name() + " has un" + \
             self.service.verb_shared + " a " + self.service.noun_post + \
             " from our " + self.service.name + " account! I hope you weren't too attached " + \
             "to it!\nUn" + self.service.verb_shared + " " + self.service.noun_post + \
             ": " + self.unshared_post_url
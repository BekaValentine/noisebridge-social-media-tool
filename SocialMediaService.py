class SocialMediaService:
  def __init__(self):
    self.name = "SocialMediaService"
    self.verb_made = "made"
    self.verb_shared = "shared"
    self.noun_post = "post"
  
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
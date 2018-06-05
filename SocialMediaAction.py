class SocialMediaAction:
  
  def __init__(self, user_id):
    self.user_id = user_id
    self.icon_emoji = ":vibration_mode:"
  
  def handle(self):
    print("Handling a social media action.")
  
  def user_name(self):
    return "<@%s>" % self.user_id
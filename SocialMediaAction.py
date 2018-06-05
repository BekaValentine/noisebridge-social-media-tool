class SocialMediaAction:
  
  def __init__(self, slack_handle):
    self.slack_handle = slack_handle
    self.icon_emoji = ":vibration_mode:"
  
  def handle():
    print("Handling a social media action.")
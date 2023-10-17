from slack import WebClient
from slackeventsapi import SlackEventAdapter

from config import settings

slack_signing_secret = settings.SLACK_SIGNING_SECRET
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/api/v1/slack-bot")
client = WebClient(token=settings.SLACK_TOKEN)

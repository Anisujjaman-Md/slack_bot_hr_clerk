from slack.errors import SlackApiError
from rest_framework.response import Response
from rest_framework import viewsets
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import datetime

from config import settings

x = datetime.datetime.now()


class BotViewSet(viewsets.ViewSet):
    slack_signing_secret = settings.SLACK_SIGNING_SECRET
    slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/api/test")

    def create(self, request):
        client = WebClient(token=settings.SLACK_TOKEN)
        bot = client.api_call("auth.test")['user_id']
        event_data = request.data
        event = event_data.get("event")

        response_data = {"challenge": "not Found"}

        if event:
            channel_id = event.get("channel")
            user_id = event.get("user")
            message = f"Hello, <@{user_id}>! I'm your Slack bot. Current Time is {x} :("

            if bot != user_id:
                try:
                    client.chat_postMessage(channel=channel_id, text=message)
                    response_data = {"message_sent": True}
                except SlackApiError as e:
                    response_data = {"error": e.response["error"]}

        if "challenge" in event_data:
            response_data = {"challenge": event_data["challenge"]}

        return Response(response_data)

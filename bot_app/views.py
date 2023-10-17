from rest_framework.utils import json
from rest_framework.response import Response
from rest_framework import viewsets, status
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from bot_app.services import LeaveApplicationService, LeaveReportService
from config import settings
from leave_management.models import LeaveApplication


class BotViewSet(viewsets.ViewSet):
    slack_signing_secret = settings.SLACK_SIGNING_SECRET
    slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/api/v1/slack-bot")

    def create(self, request):
        client = WebClient(token=settings.SLACK_TOKEN)
        bot = client.api_call("auth.test")['user_id']
        event_data = request.data
        event = event_data.get("event")
        response_data = {"challenge": "not Found"}
        if event:
            original_text = event.get("text").upper()
            text = original_text.split(' ').pop(0)
            channel_id = event.get("channel")
            user_id = event.get("user")
            if bot != user_id:
                if text == "LEAVE":
                    eligible = LeaveApplicationService().check_how_many_leave_taken(event, channel_id)
                    if eligible is True:
                        LeaveApplicationService().leave_form(event, channel_id)
                if text == "REPORT":
                    LeaveReportService().leave_report(event, channel_id)

        if "challenge" in event_data:
            response_data = {"challenge": event_data["challenge"]}

        return Response(response_data, status=status.HTTP_200_OK)


class BotFormViewSet(viewsets.ViewSet):
    def create(self, request):
        client = WebClient(token=settings.SLACK_TOKEN)
        bot = client.api_call("auth.test")['user_id']
        payload = request.POST.get("payload")
        if payload:
            data = json.loads(payload)
            employee_id = data.get("user", {}).get("id", {})
            employee_name = data.get("user", {}).get("username", {})
            action_id = data.get("actions", [])[0].get("action_id")
            channel_id = data.get("channel", {}).get("id", {})
            values = data["state"]["values"]
            if action_id == "submit_form_action":
                leave_type = values["sectionBlockWithStaticSelect"]["leave_type_block_action"]["selected_option"][
                    "value"]
                start_date = values["sectionBlockWithStartDate"]["start_date_action"]["selected_date"]
                end_date = values["sectionBlockWithEndDate"]["end_date_action"]["selected_date"]
                comment = values["sectionBlockWithComment"]["comment_input"]["value"]

                LeaveApplication.objects.create(employee_id=employee_id, employee_name=employee_name,
                                                leave_type=leave_type, start_date=start_date, end_date=end_date,
                                                comment=comment, channel_id=channel_id)
                if bot != employee_id:
                    client.chat_postMessage(channel=channel_id, text=f'Hey <@{employee_id}>, Your leave application '
                                                                     f'submitted. Please wait '
                                                                     'for approval notification')
            return Response({"message": "Data received and processed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Payload is empty."}, status=status.HTTP_400_BAD_REQUEST)

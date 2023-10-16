from rest_framework.utils import json
from slack.errors import SlackApiError
from rest_framework.response import Response
from rest_framework import viewsets, status
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from bot_app.services import LeaveApplicationService
from config import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        message = ''
        if event:
            original_text = event.get("text").upper()
            text = original_text.split(' ').pop(0)
            channel_id = event.get("channel")
            user_id = event.get("user")
            if event.get("type") == "block_actions":
                LeaveApplicationService().form_data(event_data)
            if bot != user_id:
                if text == "LEAVE":
                    LeaveApplicationService().leave_message(event, channel_id)

                if text == "REPORT":
                    message = LeaveApplicationService().leave_report(event)

                if message:
                    try:
                        client.chat_postMessage(channel=channel_id, text=message)
                        response_data = {"message_sent": True}
                    except SlackApiError as e:
                        response_data = {"error": e.response["error"]}

        if "challenge" in event_data:
            response_data = {"challenge": event_data["challenge"]}

        return Response(response_data, status=status.HTTP_200_OK)


@csrf_exempt
def slack_interaction(request):
    if request.method == "POST":
        payload = request.POST.get("payload")
        if payload:
            data = json.loads(payload)
            employee_id = data.get("user", {}).get("id")
            employee_name = data.get("user", {}).get("name", {})
            action_id = data.get("actions", [])[0].get("action_id")
            values = data["state"]["values"]
            if action_id == "submit_form_action":
                leave_type = values["sectionBlockWithStaticSelect"]["leave_type_block_action"]["selected_option"]["value"]
                start_date = values["sectionBlockWithStartDate"]["start_date_action"]["selected_date"]
                end_date = values["sectionBlockWithEndDate"]["end_date_action"]["selected_date"]
                comment = values["sectionBlockWithComment"]["comment_input"]["value"]
                LeaveApplication.objects.create(employee_id=employee_id, employee_name=employee_name,
                                                leave_type=leave_type, start_date=start_date, end_date=end_date,
                                                comment=comment)
            return JsonResponse({"message": "Data received and processed successfully."})
        else:
            return JsonResponse({"message": "Payload is empty."}, status=400)
    else:
        return JsonResponse({"message": "Invalid request method."}, status=400)

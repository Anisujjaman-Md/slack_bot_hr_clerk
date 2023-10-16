from datetime import datetime

from slack.errors import SlackApiError
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from config import settings

slack_signing_secret = settings.SLACK_SIGNING_SECRET
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/api/v1/slack-bot")
client = WebClient(token=settings.SLACK_TOKEN)


class LeaveApplicationService:
    def __init__(self):
        pass

    def check_how_many_leave_taken(self, event, channel_id):
        pass

    def leave_message(self, event, channel_id):
        user_id = event.get("user")
        current_date = datetime.now().strftime("%Y-%m-%d")
        leave_type_block = {
            "type": "section",
            "block_id": "sectionBlockWithStaticSelect",
            "text": {
                "type": "mrkdwn",
                "text": "Pick the type of leave you need:"
            },
            "accessory": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": True
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Vacation",
                            "emoji": True
                        },
                        "value": "VACATION"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Sick",
                            "emoji": True
                        },
                        "value": "SICK_LEAVE"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "Maternity Leave",
                            "emoji": True
                        },
                        "value": "MATERNITY_LEAVE"
                    }
                ],
                "action_id": "leave_type_block_action"
            }
        }

        start_date_block = {
            "type": "section",
            "block_id": "sectionBlockWithStartDate",
            "text": {
                "type": "mrkdwn",
                "text": "Pick a start date:"
            },
            "accessory": {
                "type": "datepicker",
                "initial_date": current_date,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True
                },
                "action_id": "start_date_action"
            }
        }

        end_date_block = {
            "type": "section",
            "block_id": "sectionBlockWithEndDate",
            "text": {
                "type": "mrkdwn",
                "text": "Pick an end date:"
            },
            "accessory": {
                "type": "datepicker",
                "initial_date": current_date,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a date",
                    "emoji": True
                },
                "action_id": "end_date_action"
            }
        }

        comment_block = {
            "type": "input",
            "block_id": "sectionBlockWithComment",
            "element": {
                "type": "plain_text_input",
                "action_id": "comment_input",
                "multiline": True,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Type your comment here"
                }
            },
            "label": {
                "type": "plain_text",
                "text": "Comment"
            }
        }

        send_button_block = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Submit",
                        "emoji": True
                    },
                    "action_id": "submit_form_action"
                }
            ]
        }
        blocks = [leave_type_block, start_date_block, end_date_block, comment_block, send_button_block]

        response = client.chat_postMessage(channel=channel_id, blocks=blocks)

    def form_data(self, payload):
        action = payload["event"]["actions"][0]

        if action["action_id"] == "actionId-0":
            user_response = action["value"]
            response = client.chat_postMessage(
                channel=payload["event"]["channel"],
                text=f"Thanks for your response: {user_response}"
            )

    def leave_report(self, event):
        user_id = event.get("user")
        text = event.get("text")[7:]

        message = f"Hello, <@{user_id}>!This is your report for {text}"
        return message
